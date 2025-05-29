import datetime

import polars as pl
import streamlit as st
from google.cloud.firestore import Client as FirestoreClient

from config import settings


def load_weight_log() -> pl.DataFrame:
    """Firestoreから体重ログを取得する

    Returns:
        pl.DataFrame: 体重ログ
    """
    db = FirestoreClient(project=settings.PROJECT_ID, database=settings.DATABASE)
    docs = db.collection(settings.COLLECTION).stream()
    data = [{**doc.to_dict(), "date": doc.id} for doc in docs]

    return pl.from_records(data)


def save_weight_log(date: datetime.date, weight: int, intake: int, message: str) -> None:
    """Firestoreに体重ログを保存

    Args:
        date (datetime): 日付
        weight (int): 体重
        intake (int): 食事量
        message (str): メモ
    """
    db = FirestoreClient(project=settings.PROJECT_ID, database=settings.DATABASE)
    db.collection(settings.COLLECTION).document(date.strftime("%Y-%m-%d")).set(
        {
            "weight": weight,
            "intake": intake,
            "message": message,
        }
    )


if __name__ == "__main__":
    st.set_page_config(page_title="毎日くうちゃん")
    st.title("毎日くうちゃん")

    st.session_state["weight_log_df"] = load_weight_log()

    # input form
    with st.container(border=True):
        cols = st.columns(4)
        with cols[0]:
            date = st.date_input("日付", value=datetime.datetime.today())
        with cols[1]:
            weight = st.number_input("体重 (g)", value=0, step=1)
        with cols[2]:
            intake = st.number_input("食事量 (g)", value=0, step=1)
        with cols[3]:
            message = st.text_input("memo", value="")

        submit = st.button("保存")
        if submit:
            save_weight_log(date, weight, intake, message)
            st.toast("保存しました", icon="🎉")
            st.session_state["weight_log_df"] = load_weight_log()

    st.line_chart(
        data=st.session_state["weight_log_df"],
        x="date",
        y=["weight", "intake"],
        x_label="日付",
        y_label="体重",
    )
