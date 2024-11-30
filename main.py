import numpy as np
import streamlit as st

def generate_pairs(names, constraints):
    np_names = np.array(names)
    valid = False
    attempts = 0
    max_attempts = 1000  # Prevent infinite loops
    
    while not valid and attempts < max_attempts:
        attempts += 1
        np_shuffled = np_names.copy()
        np.random.shuffle(np_shuffled)
        
        valid = True
        for constraint in constraints:
            idx0 = np.where(np_shuffled == constraint[0])[0][0]
            idx1 = np.where(np_shuffled == constraint[1])[0][0]
            if abs(idx0 - idx1) == 1 or abs(idx0 - idx1) == len(np_shuffled) - 1:
                valid = False
                break
    
    if attempts >= max_attempts:
        return None
    
    # Generate pairs
    pairs = []
    for i in range(len(np_shuffled) - 1):
        pairs.append((np_shuffled[i], np_shuffled[i + 1]))
    pairs.append((np_shuffled[-1], np_shuffled[0]))  # Connect last to first
    
    return pairs

def main():
    # Page config and styling
    st.set_page_config(
        page_title="Secret Santa Generator",
        page_icon="🎅",
        layout="centered"
    )

    # Custom CSS
    st.markdown("""
        <style>
        .stTitle {
            color: #ff0000;
            text-align: center;
            font-size: 3rem !important;
            padding: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .stHeader {
            color: #ffffff;
        }
        .participant-card {
            background-color: #ff0000;
            color: #ffffff;
            padding: 0.5rem;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            margin: 0.2rem;
            font-weight: bold;
            transition: transform 0.2s;
        }
        .participant-card:hover {
            transform: scale(1.02);
        }
        .constraint-item {
            background-color: #1b4d1b;
            padding: 0.5rem;
            border-radius: 5px;
            margin: 0.2rem;
            color: #ffffff;
            border: 1px solid #ff0000;
        }
        .result-card {
            background-color: #1b4d1b;
            color: #ffffff;
            padding: 1rem;
            border-radius: 10px;
            margin: 0.5rem;
            border: 2px solid #ff0000;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            transition: transform 0.2s;
        }
        .result-card:hover {
            transform: scale(1.01);
        }
        </style>
    """, unsafe_allow_html=True)

    # Title with festive emojis
    st.markdown("# 🎅 Secret Santa Pair Generator 🎄")
    st.markdown("---")

    # Sidebar with info
    with st.sidebar:
        st.markdown("### ℹ️ How to Use")
        st.markdown("""
        1. Enter participant names
        2. Add any pairing constraints
        3. Click generate to create pairs!
        
        ### 🎁 Tips
        - One name per line
        - Add constraints for people who shouldn't be paired
        - Clear constraints to start over
        """)

    # Input section for names with festive container
    st.markdown("### 🎯 Participants")
    with st.container():
        names_text = st.text_area(
            "Enter names (one per line)",
            value="Theo\nEls\nNico\nOpa\nOma\nAnton\nFeliz\nVictor\nJeroen\nNathalie\nAlisa\nMalou",
            height=200
        )
        names = [name.strip() for name in names_text.split('\n') if name.strip()]

    # Display names in a grid with custom styling
    st.markdown("### 📋 Current Participants")
    cols = st.columns(4)
    for i, name in enumerate(names):
        cols[i % 4].markdown(f"""
            <div class='participant-card'>
                🎄 {name}
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Constraints section with improved UI
    st.markdown("### ⚡ Constraints")
    st.info("Select pairs that should not be adjacent in the gift exchange")

    constraints = []
    col1, col2, col3 = st.columns([2,2,1])

    with col1:
        person1 = st.selectbox("First Person 👤", names, key="person1")
    with col2:
        person2_options = [n for n in names if n != person1]
        person2 = st.selectbox("Second Person 👤", person2_options, key="person2")
    with col3:
        if st.button("Add ➕", use_container_width=True):
            if [person1, person2] not in constraints:
                st.session_state.setdefault('constraints', []).append([person1, person2])

    # Display current constraints with custom styling
    if 'constraints' in st.session_state:
        st.markdown("### 📝 Current Constraints")
        for c in st.session_state.constraints:
            st.markdown(f"""
                <div class='constraint-item'>
                    ❌ {c[0]} cannot be paired with {c[1]}
                </div>
            """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([4,1])
        with col2:
            if st.button("Clear All 🗑️"):
                st.session_state.constraints = []

    st.markdown("---")

    # Generate pairs with enhanced UI
    if st.button("🎲 Generate Pairs!", use_container_width=True):
        current_constraints = st.session_state.get('constraints', [])
        pairs = generate_pairs(names, current_constraints)
        
        if pairs:
            st.balloons()
            st.success("🎉 Successfully generated pairs!")
            st.markdown("### 🎁 Results")
            for giver, receiver in pairs:
                st.markdown(f"""
                    <div class='result-card'>
                        🎁 <b>{giver}</b> → 🎄 <b>{receiver}</b>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.error("😕 Could not find a valid arrangement with these constraints. Try reducing the number of constraints.")

    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: gray; padding: 1rem;'>
            🎄 Made with ❤️ for Secret Santa 🎅
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
