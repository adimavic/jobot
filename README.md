# Jobot  

**A Python-based application designed to streamline job searching by automating the process of finding HR emails for job openings.**  

---

## Overview  

Jobot is built to simplify the job search process by:  

- **Scraping the web** to find job-related posts and extract HR email addresses.  
- Sending **customized emails** to HRs directly, saving users from manually drafting and sending emails repeatedly.  
- **Cold emailing made easy**, helping users reach out to recruiters efficiently.  

**Disclaimer**:  
While Jobot does not guarantee job offers, it ensures you are shortlisted for relevant profiles, provided you use the tool effectively.  

---

## Features  

- **Web Scraping for HR Emails**: Automatically searches Google for job-related posts and extracts HR contact information.  
- **Automated Emailing**: Sends personalized emails to HRs based on user-defined parameters.  
- **Customizable Configuration**: The application uses a `config.json` file for flexible email settings.  

---

## Purpose  

The application was created to:  
- **Help job seekers** automate the tedious process of finding and emailing HRs.  
- Reduce the need to visit multiple websites and job portals.  
- Ensure job seekers focus more on interview preparation rather than repetitive tasks.  

---

## Prerequisites  

1. **Python 3.x**: Required to run the bot.  
2. **Gmail Account**:  
   - Enable **"Less Secure App Access"** or use an **App Password** for secure email-sending capabilities.  

---

## Installation  

1. **Clone the Repository**:  
   ```bash  
   git clone https://github.com/adimavic/jobot.git  
   cd jobot  
   ```  

2. **Install Dependencies**:  
   Use a virtual environment to manage dependencies.  
   ```bash  
   python3 -m venv venv  
   source venv/bin/activate  # On Windows, use venv\Scripts\activate  
   pip install -r requirements.txt  
   ```  

3. **Configure the Application**:  
   Edit the `config.json` file in the project root directory:  
   ```json  
   {  
       "email": "your_email_address",  
       "app_password": "your_email_app_password",  
       "subject": "Subject of the email",  
       "body": "Body of the email"  
   }  
   ```  

---

## Usage  

1. **Start the Application**:  
   ```bash  
   python main.py  
   ```  

2. **Set Your Job Preferences**:  
   Modify the job-related keywords and location preferences in the script (or as prompted).  

3. **Send Cold Emails**:  
   Jobot will:  
   - Search Google for relevant job openings.  
   - Extract HR email addresses from the posts.  
   - Send customized emails to the identified HR contacts based on the `config.json` settings.  

---

## Hunter.io Integration (Optional)  

You can enhance email validation and accuracy by integrating **Hunter.io**. This improves the success rate of your cold emails significantly.  

---

## Disclaimer  

This application is intended to assist in job searching by automating certain tasks. However:  
- It does not guarantee job offers.  
- Users must ensure their emails are well-crafted and follow professional etiquette to increase their chances of being shortlisted.  

---

## Acknowledgements  

- Created to help job seekers focus more on interview preparation and less on manual emailing tasks.  
- Inspired by the power of automation and the effectiveness of cold emailing when combined with tools like Hunter.io.  

---  
