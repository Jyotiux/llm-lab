import streamlit as st
from agent import graph  # Import the graph from agent.py

# Streamlit app UI
st.title("📚 Research Assistant AI")

# User input
user_input = st.text_input("Ask me anything about research:")

# Button to submit the query
if st.button("Submit"):
    if user_input:
        with st.spinner("Fetching response..."):
            # Call the agent to process the input
            response = graph.invoke({"messages": user_input})

            # Check if the response contains "messages"
            if isinstance(response, dict) and "messages" in response:
                messages = response["messages"]
                for msg in messages:
                    # Directly access the content from HumanMessage or AIMessage objects
                    content = msg.content if hasattr(msg, 'content') else None
                    if content:
                        st.write(content)  # Display the content only
                    else:
                        st.write("No content found in the response.")
            else:
                st.warning("No messages found in the response.")
    else:
        st.warning("Please enter a question.")


