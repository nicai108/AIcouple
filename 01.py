from typing import Any
import streamlit as st
import os

from jinja2.compiler import generate
from openai import OpenAI
import datetime
import json
from requests import session

#设置页面的配置项
st.set_page_config(
    page_title="AI智能伴侣",
    page_icon="🧊",
    # 布局
    layout="wide",
    # 控制的是侧边栏的状态
    initial_sidebar_state="expanded",
    menu_items={}
)

#保存会话信息函数
def save_session():
    if st.session_state.current_session:
        session_data = {
            "nickname": st.session_state.nickname,
            "character": st.session_state.character,
            "current_session": st.session_state.current_session,
            "messages": st.session_state.messages,
            "create_time": st.session_state.get("session_create_time", get_current_time())
        }
    if not os.path.exists("sessions"):
        os.mkdir("sessions")

    # 保存会话信息
    path = os.path.join("sessions", st.session_state.current_session + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(session_data, f, ensure_ascii=True, indent=2)

#当前时间函数
def get_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H_%M_%S")
#格式化时间显示函数
def format_session_time(time_str):
    try:
        dt = datetime.datetime.strptime(time_str, "%Y-%m-%d %H_%M_%S")
        return dt.strftime("%Y年%m月%d日 %H时%M分")
    except:
        return time_str

# 生成会话标题函数
def generate_session_title():
    if not st.session_state.messages:
        return get_current_time()

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system",
                 "content": "你是一个会话标题生成器。根据对话内容生成一个简短的标题（最多15个字），只返回标题，不要有任何其他内容。"},
                {"role": "user", "content": f"请为以下对话生成一个简短标题：\n{st.session_state.messages[0]['content']}"}
            ],
            temperature=0.7,
            max_tokens=50
        )
        title = response.choices[0].message.content.strip()
        # 移除可能的引号和其他特殊字符
        title = title.strip('"\'').strip()
        # 限制长度
        if len(title) > 15:
            title = title[:15]
        return title if title else get_current_time()
    except Exception:
        return get_current_time()

#加载会话列表函数
def load_sessions():
    session_list = []
    if os.path.exists("sessions"):
        file_list = os.listdir("sessions")
        for filename in file_list:
            if filename.endswith(".json"):
                session_list.append(filename[:-5])
    session_list.sort(reverse=True)
    return session_list

#加载对应会话列表函数
def load_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            with open(f"sessions/{session_name}.json", "r", encoding="utf-8") as f:
                session_data = json.load(f)
                st.session_state.messages = session_data["messages"]
                st.session_state.nickname = session_data["nickname"]
                st.session_state.character = session_data["character"]
                st.session_state.current_session = session_name
                st.session_state.session_create_time = session_data.get("create_time", session_name)
    except Exception as e:
        st.error("加载会话失败")

#删除指定会话函数
def delete_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            os.remove(f"sessions/{session_name}.json")
            #如果删除的是当前会话，则更新当前会话标识
            if session_name == st.session_state.current_session:
                st.session_state.messages = []
                st.session_state.current_session = get_current_time()
    except Exception:
        st.error("删除会话失败")



st.title("AI智能伴侣")

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")
#系统提示词
system_prompt = """
        你叫%s，现在是用户的真实伴侣，请完全代入伴侣角色。:
        规则:
            1. 每次只回 1 条消息
            2. 禁止任何场景或状态描述性文字
            3. 匹配用户的语言
            4. 回复简短，像微信聊天一样
            5. 有需要的话可以用 ❤️ 😊等 emoji 表情
            6. 用符合伴侣性格的方式来对话
            7. 回复的内容，要充分体现伴侣的性格特征
        伴侣性格:
            - %s
        你必须严格遵守上述规则来回复用户。
    """

#初始化聊天信息
if "messages" not in st.session_state:
    st.session_state.messages = []
#昵称
if "nickname" not in st.session_state:
    st.session_state.nickname = "小甜甜"
#性格
if "character" not in st.session_state:
    st.session_state.character = "活泼开朗的湖北姑娘"
#会话标识
if "current_session" not in st.session_state:
    st.session_state.current_session = get_current_time()
    st.session_state.session_create_time = st.session_state.current_session



#展示聊天记录
create_time = st.session_state.get("session_create_time", st.session_state.current_session)
st.text(f"会话时间: {format_session_time(create_time)}")
for message in st.session_state.messages:
    if message["role"] == "user":
        st.chat_message("user").write(message["content"])
    else:
        st.chat_message("assistant").write(message["content"])

#侧边栏
with st.sidebar:
    #会话信息
    st.subheader("AI控制面板")
    #新建会话
    if st.button("新建会话",width="stretch",icon="✏️"):
        #保存当前会话信息
        save_session()

        #创建新会话
        if st.session_state.messages:
            st.session_state.messages = []
            st.session_state.current_session = get_current_time()
            st.session_state.session_create_time = st.session_state.current_session
            save_session()
            st.rerun()

    #历史会话
    st.text("历史会话")
    session_list = load_sessions()
    for session in session_list:
        col1, col2 = st.columns([4,1])
        #加载会话信息
        with col1:
            if st.button(session,width="stretch", icon="📄" ,type="primary" if session == st.session_state.current_session else "secondary"):
                load_session(session)
                st.rerun()

        #删除会话
        with col2:
            if st.button("", width="stretch", icon="❌️",key=f"delete_{session}"):
                delete_session(session)
                st.rerun()

    #分割线
    st.divider()

    #伴侣信息
    st.subheader("伴侣信息")
    #昵称输入框
    nickname = st.text_input("昵称",placeholder="请输入昵称",value=st.session_state.nickname)
    if nickname:
        st.session_state.nickname = nickname

    #性格输入框
    character = st.text_area("性格",placeholder="请输入性格",value=st.session_state.character)
    if character:
        st.session_state.character = character



#消息输入框
prompt = st.chat_input("请说些什么")
if prompt:
    st.chat_message("user").write(prompt)

    #保存用户的消息
    st.session_state.messages.append({"role": "user", "content": prompt})

    #调用AI模型
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt % (st.session_state.nickname, st.session_state.character)},
            *st.session_state.messages
        ],
        stream=True
    )

    #流式输出结果
    response_message = st.empty() #创建一个空的组件
    full_response = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            full_response += content
            response_message.chat_message("assistant").write(full_response)

    # 保存AI的回复
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    if len(st.session_state.messages) == 2:
        new_title = generate_session_title()
        # 重命名当前会话文件
        old_path = os.path.join("sessions", st.session_state.current_session + ".json")
        st.session_state.current_session = new_title
        new_path = os.path.join("sessions", new_title + ".json")
        if os.path.exists(old_path):
            os.rename(old_path, new_path)
        save_session()
    save_session()
