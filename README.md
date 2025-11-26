# 💻 Laptop Preference Agent (NPD Project)

This is an AI-powered web chatbot designed to analyze user preferences for laptops. It helps in New Product Development (NPD) by matching user needs (Price, Processor, Screen, etc.) with available market options.

## 📂 Files in this Repository
* `app.py`: The main Python script containing the chatbot logic.
* `requirements.txt`: List of libraries needed to run the app.
* `laptops.csv`: The dataset containing laptop models and specifications.

## 🚀 How to Run Locally
1.  Install Python and Streamlit.
2.  Run the command:
    ```bash
    streamlit run app.py
    ```

## 🌐 Deployment (Hugging Face Spaces)
This project is deployed using Streamlit on Hugging Face Spaces.
1.  Connect this GitHub repository to a new Space.
2.  Select **Streamlit** as the SDK.
3.  The app will automatically install dependencies from `requirements.txt` and launch.

## 📊 Features
* **Purpose Analysis:** Filters by Gaming, Student, Office, or Creative use.
* **Budget Filtering:** Matches laptops within specific price ranges (INR).
* **Tech Specs:** Filters by Processor Brand (Intel/AMD) and Screen Type (IPS/OLED).
* **Recommendation:** Displays the top 5 matches sorted by rating.
