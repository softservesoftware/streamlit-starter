import streamlit as st
from utils.authentication import log_activity
import os


@log_activity
def render():
    st.title("About")
    st.markdown(
        """

        ---

        ## About Streamlit Starter

        Streamlit Starter is an open-source project designed to help you **launch your data-driven ideas faster than ever**. By providing a ready-to-use boilerplate, it eliminates the hassle of setting up and configuring your development environment, so you can focus on building incredible applications.

        ---

        ## Why Did I Create Streamlit Starter?

        I understand the challenges of turning an idea into a reality. From setting up infrastructure to managing the complexities of deployment, the process can be overwhelming. That's why I built Streamlit Starter—to simplify this journey by providing a **scalable, modular, and extensible framework** tailored to your needs.

        Whether you're an entrepreneur building your MVP, a data scientist sharing insights, or a software engineer looking for streamlined solutions, Streamlit Starter can save you **time**, **effort**, and **headaches**.

        ---

        ## My Goal

        I aim to create tools, frameworks, and solutions that:

        - Enable you to **focus on innovation** rather than setup and infrastructure.
        - Accelerate your **time-to-market** for ideas and projects.
        - Make technology accessible to everyone, regardless of technical background.

        By bridging the gap between vision and execution, I hope to inspire and empower others to turn their ideas into reality.

        ---

        ## Let's Build Together

        I’m always open to collaboration, feedback, and suggestions. Together, we can build tools that simplify development, enhance productivity, and drive innovation. Let’s make your next big idea happen—faster and better than ever before.

        [Contact me](https://calendly.com/mattdvertola/30min) if you need help building your next project or have ideas for collaboration.

        """
    )
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(
            """
        ## Who Am I?
        Hi, I'm Matt Dvertola—a Software Engineer and Data Scientist passionate about empowering professionals to bring their ideas to life. My mission is to help entrepreneurs, software engineers, data scientists, and other savvy professionals **launch their ideas, build automations**, and create solutions that make an impact.
        """
        )
    with col2:
        st.image(f"{os.getcwd()}/static/matt.webp")


render()
