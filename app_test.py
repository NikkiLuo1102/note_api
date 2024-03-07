import pytest
from app import app
from datetime import datetime


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_create_delete_note(client):
    # 首先创建一个笔记
    create_data = {
        "username": "deletetest",
        "color": "Red",
        "content": "test for delete",
        "time": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    }
    response = client.post("/create_note", json=create_data)
    assert response.status_code == 201
    assert response.json == {"message": "Note created successfully"}

    # 获取新创建的笔记的 ID
    response = client.get("/retrieve_notes?username=deletetest")
    note_id = response.json[0]["note_id"]

    # 准备请求数据
    data = {
        "note_id": note_id
    }

    # 发送 POST 请求
    response = client.post("/delete_note", json=data)

    # 检查状态码是否为 200
    assert response.status_code == 200

    # 检查返回消息是否正确
    assert response.json == {"message": "Note deleted successfully"}


def test_retrieve_notes(client):
    # 模拟请求参数
    username = "nikkitest"

    # 发送 GET 请求
    response = client.get(f"/retrieve_notes?username={username}")

    # 检查状态码是否为 200
    assert response.status_code == 200


def test_update_note(client):
    # 准备请求数据
    data = {
        "note_id": 4,
        "color": "Blue",
        "content": "test for update",
        "time": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    }

    # 发送 POST 请求
    response = client.post("/update_note", json=data)

    # 检查状态码是否为 200
    assert response.status_code == 200

    # 检查返回消息是否正确
    assert response.json == {"message": "Note updated successfully"}
