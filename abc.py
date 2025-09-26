import streamlit as st

# Initialize session state to persist balances and transactions
if "students" not in st.session_state:
    st.session_state.students = {
        "Alice": 0,
        "Bob": 0,
        "Charlie": 0,
        "Diana": 0
    }

st.title("💰 EduCoin Classroom Cryptocurrency")

# --- Teacher Panel ---
st.header("Teacher Panel: Mint EduCoins")

student_to_mint = st.selectbox("Select student to reward 1 EduCoin:", list(st.session_state.students.keys()))

if st.button("Mint 1 EduCoin"):
    st.session_state.students[student_to_mint] += 1
    st.success(f"Minted 1 EduCoin to {student_to_mint}")

st.markdown("---")

# --- Student Panel ---
st.header("Student Panel: Check Balance & Transfer EduCoins")

student_wallet = st.selectbox("Select your wallet:", list(st.session_state.students.keys()), key="wallet")

st.write(f"Your current balance: **{st.session_state.students[student_wallet]}** EduCoin(s)")

recipient = st.selectbox("Transfer to:", [s for s in st.session_state.students if s != student_wallet])

amount = st.number_input(
    "Amount to transfer:",
    min_value=1,
    max_value=st.session_state.students[student_wallet],
    step=1,
    value=1
)

if st.button("Send EduCoins"):
    if amount <= st.session_state.students[student_wallet]:
        st.session_state.students[student_wallet] -= amount
        st.session_state.students[recipient] += amount
        st.success(f"Transferred {amount} EduCoin(s) to {recipient}")
    else:
        st.error("Insufficient balance to complete this transfer.")

st.markdown("---")

# --- Leaderboard ---
st.header("Leaderboard: Top EduCoin Holders")

sorted_students = sorted(st.session_state.students.items(), key=lambda x: x[1], reverse=True)

for rank, (name, balance) in enumerate(sorted_students, start=1):
    st.write(f"{rank}. {name} — **{balance} EduCoin(s)**")

