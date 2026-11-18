#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/10/10 18:27
@Author : 751363075@qq.com
@File : 2.从本地文件夹加载文件存入faiss向量数据库.py
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/10/10
@Author : 751363075@qq.com
@File : faiss_service.py
@Description : LLMOps API接口文档向量化及 FAISS 向量库管理
"""

import os
import logging
from pathlib import Path
from typing import List, Optional, Tuple, Any

import dotenv
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

logger = logging.getLogger(__name__)

# 当前文件位于项目根目录/internal/core/faiss_service.py
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# 原始 Markdown 文档所在目录
STORAGE_DIR = PROJECT_ROOT / "storage"

# FAISS 向量库保存目录
VECTOR_STORE_DIR = PROJECT_ROOT / "internal" / "core" / "vector_store"

# 目标 Markdown 文档名称
DOCUMENT_NAME = "LLMOps API接口文档.md"

# 文本切割参数
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


class FaissService:
    """FAISS 向量库服务。"""

    def __init__(self):
        """初始化 Embedding 模型及相关配置。"""
        dotenv.load_dotenv(PROJECT_ROOT / ".env")

        self.embeddings = HuggingFaceEmbeddings(
            model_name="Alibaba-NLP/gte-multilingual-base",
            cache_folder=os.path.join(os.getcwd(), "internal", "core", "embeddings"),
            model_kwargs={
                "trust_remote_code": True,
            },
        )

        self.vector_store: Optional[FAISS] = None

    @staticmethod
    def find_document() -> Path:
        """
        递归查找目标 Markdown 文档。

        Returns:
            Path: 文档的绝对路径。
        """
        if not STORAGE_DIR.exists():
            raise FileNotFoundError(
                f"文档目录不存在：{STORAGE_DIR}"
            )

        matched_files = list(
            STORAGE_DIR.rglob(DOCUMENT_NAME)
        )

        if not matched_files:
            raise FileNotFoundError(
                f"未找到文档：{STORAGE_DIR / '**' / DOCUMENT_NAME}"
            )

        if len(matched_files) > 1:
            paths = "\n".join(
                str(path) for path in matched_files
            )
            raise ValueError(
                f"找到多个同名文档，请保留一个或明确指定路径：\n{paths}"
            )

        return matched_files[0]

    @staticmethod
    def load_markdown(file_path: Path) -> str:
        """
        读取 Markdown 文件。

        utf-8-sig 同时兼容带 BOM 的 UTF-8 文件。
        """
        content = file_path.read_text(
            encoding="utf-8-sig"
        ).strip()

        if not content:
            raise ValueError(
                f"Markdown 文档内容为空：{file_path}"
            )

        return content

    @staticmethod
    def split_document(
            content: str,
            source_path: Path,
    ) -> List[Document]:
        """
        将 Markdown 文档切割为文本块。

        使用标题、段落和中文标点等作为切割边界，
        并为每个文本块设置元数据。
        """
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len,
            separators=[
                "\n# ",
                "\n## ",
                "\n### ",
                "\n#### ",
                "\n```",
                "\n\n",
                "\n",
                "。 ",
                "。\n",
                "！",
                "？",
                "；",
                "，",
                " ",
                "",
            ],
        )

        chunks = splitter.split_text(content)

        if not chunks:
            raise ValueError("Markdown 文档切割结果为空")

        documents = []

        for index, chunk in enumerate(chunks):
            documents.append(
                Document(
                    page_content=chunk,
                    metadata={
                        "source": str(source_path),
                        "file_name": source_path.name,
                        "chunk_index": index,
                        "chunk_count": len(chunks),
                    },
                )
            )

        logger.info(
            "文档切割完成，文件：%s，分块数量：%s",
            source_path,
            len(documents),
        )

        return documents

    def create_vector_store(
            self,
            overwrite: bool = True,
    ) -> FAISS:
        """
        创建 FAISS 向量库并保存到本地。

        Args:
            overwrite: 是否重建现有向量库。
                True：重新生成整个向量库。
                False：如果已有索引，则拒绝覆盖。

        Returns:
            FAISS: 已构建的向量库。
        """
        index_file = VECTOR_STORE_DIR / "index.faiss"

        if index_file.exists() and not overwrite:
            raise FileExistsError(
                f"向量库已存在：{VECTOR_STORE_DIR}"
            )

        # 1. 查找并读取文档
        document_path = self.find_document()
        content = self.load_markdown(document_path)

        logger.info("开始处理文档：%s", document_path)

        # 2. 切割文档
        documents = self.split_document(
            content=content,
            source_path=document_path,
        )

        # 3. 调用 Embedding 模型生成向量并构建 FAISS
        vector_store = FAISS.from_documents(
            documents=documents,
            embedding=self.embeddings,
        )

        # 4. 保存到项目根目录下的 vector_store
        VECTOR_STORE_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        vector_store.save_local(
            str(VECTOR_STORE_DIR)
        )

        self.vector_store = vector_store

        logger.info(
            "向量库创建成功，文本块数量：%s，保存目录：%s",
            vector_store.index.ntotal,
            VECTOR_STORE_DIR,
        )

        return vector_store

    def load_vector_store(
            self,
            allow_dangerous_deserialization: bool = False,
    ) -> FAISS:
        """
        加载本地 FAISS 向量库。

        注意：
        index.pkl 使用 pickle 反序列化。
        只有在确认索引文件来源可信时，才应开启
        allow_dangerous_deserialization。
        """
        index_file = VECTOR_STORE_DIR / "index.faiss"
        pickle_file = VECTOR_STORE_DIR / "index.pkl"

        if not index_file.exists() or not pickle_file.exists():
            raise FileNotFoundError(
                f"向量库文件不完整，请先创建向量库："
                f"{VECTOR_STORE_DIR}"
            )

        if not allow_dangerous_deserialization:
            raise ValueError(
                "加载 FAISS 需要反序列化本地 index.pkl。"
                "请确认文件来源可信后，显式设置 "
                "allow_dangerous_deserialization=True。"
            )

        self.vector_store = FAISS.load_local(
            str(VECTOR_STORE_DIR),
            self.embeddings,
            allow_dangerous_deserialization=True,
        )

        logger.info(
            "向量库加载成功，当前向量数量：%s",
            self.vector_store.index.ntotal,
        )

        return self.vector_store

    def similarity_search(
            self,
            query: str,
            k: int = 4,
    ) -> List[Document]:
        """
        执行相似度检索。

        Args:
            query: 用户查询内容。
            k: 返回最相关的文本块数量。
        """
        if not query.strip():
            raise ValueError("查询内容不能为空")

        if self.vector_store is None:
            self.load_vector_store(
                allow_dangerous_deserialization=True
            )

        return self.vector_store.similarity_search(
            query=query,
            k=k,
        )

    def similarity_search_with_scores(
            self,
            query: str,
            k: int = 4,
    ) -> List[Tuple[Document, float]]:
        """
        检索文本块并返回 FAISS 原始距离分数。

        注意：FAISS 原始分数通常是距离，具体含义取决于
        向量库的距离策略，不能直接当作相似度百分比。
        """
        if not query.strip():
            raise ValueError("查询内容不能为空")

        if self.vector_store is None:
            self.load_vector_store(
                allow_dangerous_deserialization=True
            )

        return self.vector_store.similarity_search_with_score(
            query=query,
            k=k,
        )

    def add_texts(
            self,
            texts: List[str],
            metadatas: Optional[List[dict]] = None,
    ) -> List[str]:
        """向已有向量库新增文本并保存。"""
        if not texts:
            raise ValueError("待添加的文本列表不能为空")

        if self.vector_store is None:
            self.load_vector_store(
                allow_dangerous_deserialization=True
            )

        ids = self.vector_store.add_texts(
            texts=texts,
            metadatas=metadatas,
        )

        self.vector_store.save_local(
            str(VECTOR_STORE_DIR)
        )

        return ids

    def delete_by_ids(
            self,
            ids: List[str],
    ) -> bool:
        """根据 FAISS 文档 ID 删除文本并保存。"""
        if not ids:
            return False

        if self.vector_store is None:
            self.load_vector_store(
                allow_dangerous_deserialization=True
            )

        result = self.vector_store.delete(ids=ids)

        self.vector_store.save_local(
            str(VECTOR_STORE_DIR)
        )

        return bool(result)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s %(levelname)s "
            "%(name)s: %(message)s"
        ),
    )

    service = FaissService()

    # 首次运行：切割 Markdown、生成向量并保存。
    db = service.create_vector_store(overwrite=True)

    print("向量库目录：", VECTOR_STORE_DIR)
    print("向量总数：", db.index.ntotal)

    # 测试检索
    results = service.similarity_search_with_scores(
        query="如何调用 LLMOps API 接口？",
        k=4,
    )

    for document, score in results:
        print("=" * 80)
        print("分块编号：", document.metadata.get("chunk_index"))
        print("文档来源：", document.metadata.get("source"))
        print("原始距离：", score)
        print("文本内容：\n", document.page_content)
