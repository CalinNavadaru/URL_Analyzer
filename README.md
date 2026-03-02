# URL_Analyzer

## What does the app do?

Analyzes URLs in order to find out if they phishing attempts or not.

1. The user provides an URL to be analyzed;
2. The URL is sent to an analysis server that hosts an intelligent URL phishing detection model;
3. It analyzes the URL, storing data for future use (training and fine-tuning);
4. It returns the results, giving the feedback in a simple manner;
5. Also, it offers access to results from previous analysis;

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
I defined the component to be standalone. This makes to each component handles its dependecies alone.
So, what I did? I explained to him in greater detail that my components were as he defined them, but created using
```ng g c <nume> --standalone```. After this explanation, he understood and we moved on.

2. Another thingh was that it generated some CSS code that had classes/ids that weren't defined in HTML. This was a simple fix,
seeing as I only repaired the references between the files