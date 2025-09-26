import streamlit as st
import hashlib
import pandas as pd
from datetime import datetime

# --- Blockchain helper functions ---
def hash_block(block):
    block_string = f"{block['index']}{block['timestamp']}{block['transaction']}{block['previous_hash']}"
    return hashlib.sha256(block_string.encode()).hexdigest()

def create_genesis_block():
    genesis_block = {
        "index": 0,
        "timestamp": str(datetime.now()),
        "transaction": None,
        "previous_hash": "0",
        "hash": ""
    }
    genesis_block["hash"] = hash_block(genesis_block)
    return genesis_block

def create_new_block(transaction, previous_block):
    block = {
        "index": previous_block['index'] + 1,
        "timestamp": str(datetime.now()),
        "transaction": transaction,
        "previous_hash": previous_block['hash']
    }
    block["hash"] = hash_block(block)
    return block

# --- Initialize session state ---
if "students" not in st.session_state:
    st.session_state.students = {
        "Alice": 0,
        "Bob": 0,
        "Charlie": 0,
        "Diana": 0
    }

if "teacher" not in st.session_state:
    st.session_state.teacher = "Teacher"

if "transactions" not in st.session_state:
    st.session_state.transactions = []

if "blockchain" not in st.session_state:
    st.session_state.blockchain = [create_genesis_block()]

# --- Helper to add transaction and create a new block immediately ---
def add_transaction(sender, receiver, amount):
    # Check balances for student senders
    if sender != st.session_state.teacher and st.session_state.students[sender] < amount:
        st.error(f"{sender} has insufficient balance!")
        return False

    # Create transaction record
    transaction = {
        "timestamp": str(datetime.now()),
        "sender": sender,
        "receiver": receiver,
        "amount": amount
    }

    # Update balances
    if sender != st.session_state.teacher:
        st.session_state.students[sender] -= amount
    st.session_state.students[receiver] += amount

    # Append to transactions list
    st.session_state.transactions.append(transaction)

    # Create new block with this single transaction
    previous_block = st.session_state.blockchain[-1]
    new_block = create_new_block(transaction, previous_block)
    st.session_state.blockchain.append(new_block)

    st.success(f"Transaction recorded and new block created: {sender} → {receiver} : {amount} EduCoins")
    return True

# --- Streamlit UI ---

st.title("💰 EduCoin Classroom Cryptocurrency (1 transaction per block)")

st.sidebar.header("Current Balances")
for student, balance in st.session_state.students.items():
    st.sidebar.write(f"{student}: {balance} EduCoins")

st.sidebar.markdown("---")
st.sidebar.header("Blockchain Info")
st.sidebar.write(f"Total blocks (including genesis): {len(st.session_state.blockchain)}")
st.sidebar.write(f"Total transactions: {len(st.session_state.transactions)}")

# Step 1: Teacher sending coins to student
st.header("Step 1: Teacher sends coins to Student")
teacher_name = st.text_input("Teacher's Name", value=st.session_state.teacher)
student_recipient = st.selectbox("Select Student to receive coins:", list(st.session_state.students.keys()))
coins_to_send = st.number_input("Number of coins to send:", min_value=1, step=1)

if st.button("Send Coins (Teacher → Student)"):
    st.session_state.teacher = teacher_name
    add_transaction(teacher_name, student_recipient, coins_to_send)

st.markdown("---")

# Step 2: Student sending coins to another student
st.header("Step 2: Student sends coins to Student")
student_sender = st.selectbox("Sender Student:", list(st.session_state.students.keys()), key="sender")
student_receiver = st.selectbox(
    "Receiver Student:", 
    [s for s in st.session_state.students.keys() if s != student_sender],
    key="receiver"
)
coins_transfer = st.number_input("Coins to transfer:", min_value=1, max_value=st.session_state.students[student_sender], step=1, key="amount")

if st.button("Send Coins (Student → Student)"):
    add_transaction(student_sender, student_receiver, coins_transfer)

st.markdown("---")

# Step 3: Summary of all transactions
st.header("Step 3: Transaction Summary")

if st.session_state.transactions:
    df = pd.DataFrame(st.session_state.transactions)
    st.dataframe(df)
else:
    st.write("No transactions yet.")

st.markdown("---")

# Step 4: Blockchain visualization
st.header("Step 4: Blockchain Blocks")

for block in st.session_state.blockchain:
    st.subheader(f"Block #{block['index']}")
    st.write(f"Timestamp: {block['timestamp']}")
    st.write(f"Previous Hash: {block['previous_hash']}")
    st.write(f"Hash: {block['hash']}")
    if block["transaction"]:
        st.write("Transaction:")
        st.json(block["transaction"])
    else:
        st.write("Genesis block (no transactions)")



