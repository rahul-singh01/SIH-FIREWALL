# SIH FireWall
Cross-Platform Firewall: Provides granular control over application-specific network traffic with real-time
monitoring.
Centralized Management: Web-based console for policy management, monitoring, and alerting.
AI & Blockchain Integration: AI-driven anomaly detection and blockchain for secure, tamper-proof logging

## Team Details

**Team Name:** 404_Sleep

**Team Leader:** [@Jatin Sharma](https://github.com/JatSh1804)

**Team Members:**

- **MEMBER_1** - 2022UEE4523 - [@Jatin](https://github.com/JatSh1804)
- **MEMBER_2** - 2022UEE4611 - [@Rahul](https://github.com/Rahulrahul-singh01)
- **MEMBER_3** - 2022UCA1801 - [@Aditya](https://github.com/Aditya_tiwari)
- **MEMBER_4** - 2022UIN3320 - [@Vedant](https://github.com/USERNAME)
- **MEMBER_5** - 2022UEE4513 - [@Akshata](https://github.com/USERNAME)
- **MEMBER_6** - 2022UCM2304 - [@Divyansh](https://github.com/divyanshjain122)

## Project Links

- **Presentation:** [Link](https://drive.google.com/file/d/1iMbi1fJGygDrids1jop58OL69gK8omxp/view?usp=drivesdk)
- **Video Demonstration:** [Watch Video](https://drive.google.com/file/d/1jcJ7MYBInTUQbCeqEVMkWRmlkNHCIdxM/view?usp=drive_link)
- **Source Code:** [GitHub Repository](https://github.com/rahul-singh01/SIH-FIREWALL/)


## How to run it locally ?
 - on root folder run : pip instal -r requirements.txt
   
 - Inside the frontend folder run :
 - Step 1 : run yarn to install modules
 - Step 2 : yarn dev to run vite server 

- Inside the backend Folder run :
- Step 1 : python manage.py makemigrations --settings=config.settings.development
- Step 2 : python manage.py migrate --settings=config.settings.development
- Step 3 : python manage.py runserver --setting=config.settings.development

- Inside the Agent Folder run :
- Step 1 : sudo -E $(which python) main.py start (for starting the service)
- Step 2 : sudo -E $(which python) main.py stop (for stoping the service)
- Step 3 : sudo -E $(which python) main.py restart (for restarting the service)

** GUI Access from http://localhost:8000
 - Api access endpoint http://localhost:8000/api/
 - Api access for policies http://localhost:8000/api/policies


 
