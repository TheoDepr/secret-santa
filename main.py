import numpy as np
import streamlit as st

def generate_pairs(names, constraints, families):
    np_names = np.array(names)
    valid = False
    attempts = 0
    max_attempts = 1000  # Prevent infinite loops
    
    # Add family constraints automatically
    family_constraints = []
    for family_members in families.values():
        for i in range(len(family_members)):
            for j in range(i + 1, len(family_members)):
                family_constraints.append([family_members[i], family_members[j]])
    
    all_constraints = constraints + family_constraints
    
    while not valid and attempts < max_attempts:
        attempts += 1
        np_shuffled = np_names.copy()
        np.random.shuffle(np_shuffled)
        
        valid = True
        # Check all constraints including family constraints
        for constraint in all_constraints:
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
            value="John\nJane",
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

    # Add family management section
    st.markdown("### 👨‍👩‍👧‍👦 Family Groups")
    
    # Initialize families in session state if not exists
    if 'families' not in st.session_state:
        st.session_state.families = {}
    
    # Family creation interface
    col1, col2 = st.columns([3, 1])
    with col1:
        family_name = st.text_input("Family Name", key="family_name")
    with col2:
        if st.button("Add Family ➕"):
            if family_name and family_name not in st.session_state.families:
                st.session_state.families[family_name] = []
                st.success(f"Added family: {family_name}")

    # Family member assignment
    if st.session_state.families:
        st.markdown("#### Add Family Members")
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            selected_family = st.selectbox("Select Family", list(st.session_state.families.keys()))
        with col2:
            available_members = [n.strip() for n in names_text.split('\n') 
                               if n.strip() and not any(n.strip() in f for f in st.session_state.families.values())]
            selected_member = st.selectbox("Select Member", available_members) if available_members else None
        with col3:
            if selected_member and st.button("Add Member ➕"):
                st.session_state.families[selected_family].append(selected_member)

        # Display current families
        st.markdown("#### Current Families")
        for family, members in st.session_state.families.items():
            with st.expander(f"📋 {family} ({len(members)} members)"):
                for member in members:
                    col1, col2 = st.columns([5, 1])
                    col1.markdown(f"🧑 {member}")
                    if col2.button("Remove", key=f"remove_{family}_{member}"):
                        st.session_state.families[family].remove(member)
                        st.rerun()
                if st.button("Delete Family", key=f"delete_{family}"):
                    del st.session_state.families[family]
                    st.rerun()

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
        pairs = generate_pairs(names, current_constraints, st.session_state.families)
        
        if pairs:
            st.balloons()
            st.success("🎉 Successfully generated pairs!")
            st.markdown("### 🎁 Results")
            for giver, receiver in pairs:
                # Find family affiliations
                giver_family = next((f for f, m in st.session_state.families.items() if giver in m), None)
                receiver_family = next((f for f, m in st.session_state.families.items() if receiver in m), None)
                
                family_info = ""
                if giver_family:
                    family_info += f" ({giver_family})"
                if receiver_family:
                    family_info += f" → ({receiver_family})"
                
                st.markdown(f"""
                    <div class='result-card'>
                        🎁 <b>{giver}</b>{family_info} → 🎄 <b>{receiver}</b>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.error("😕 Could not find a valid arrangement with these constraints and family groups. Try reducing the number of constraints.")

    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: gray; padding: 1rem;'>
            🎄 Made with ❤️ for Secret Santa 🎅
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
