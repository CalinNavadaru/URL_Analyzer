# URL_Analyzer

## What does the app do?

Analyzes URLs to determine whether they are phishing attempts, while offering a clean and simple UI. 
The app supports full CRUD operations: creating new URL checks, viewing paginated results, updating feedback, deleting 
entries, and re-analyzing URLs.

The app allows a user to:

1. Submit a URL for analysis;
2. Send the URL to a server hosting an intelligent phishing detection model;
3. Analyze the URL and store the results for future use (training and fine-tuning);
4. Receive a clear verdict on whether the URL is safe or a phishing attempt;
5. Browse results from previous analyses;
6. Update feedback on an analyzed URL and re-analyze it if needed.

## Which LLMs/Tools were used to build this project:

1. Angular
2. PrimeNG
3. Django
4. Django REST Framework
5. SQLite
6. PyTorch
7. PyTorch Lightning
8. python-dotenv
9. ChatGPT

## One specific "hallucination" or technical hurdle you encountered and how I prompted my way into it:

1. The LLM was pointing to a path that didn't exist in my Angular Project (```src/app/app.module.ts```) because
I defined the component to be standalone. This makes to each component handles its dependencies alone.
So, what I did? I explained to him in greater detail that my components were as he defined them, but created using
```ng g c <nume> --standalone```. After this explanation, he understood and we moved on;

2. Another thing was that it generated some CSS code that had classes/ids that weren't defined in HTML. This was a simple fix,
seeing as I only repaired the references between the files.

## Running the App

### Backend
```bash
cd Backend
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

- The backend runs at `http://localhost:8000` and serves the API endpoints.
- It is intended to be accessed **only through the frontend** running on `http://localhost:4200`.
- All interactions with the URL analysis model, feedback, deletion, and re-analyze features go through the frontend UI.
### Frontend

```bash
cd Frontend
ng serve
```

It will run on browser at localhost:4200.


## 💡 Bonus tip:

### The backend AI model uses PyTorch and can take advantage of a GPU if available. On systems without a GPU, it will run on CPU (slower).