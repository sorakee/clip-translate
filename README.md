# clip-translate
Some app I developed because I want to read some Japanese comments on X/Twitter without Google's Translator failing on me.<br/>
Works well with Textractor or other third party apps that retrieve text from games, video, etc too!<br/>
You can modify the system prompt to help you add extra information that may help you learn Japanese I guess.<br/>
Feel free to modify the code to suit your purposes.

## How to Run
1. Retrieve your API key (In this case, I use OpenRouter)
2. Create a *secrets.json* file in the same directory as main.py and add this:<br/>
```
{
  "openrouter_api_key": "INSERT YOUR API KEY HERE",
}
```
4. `pip install -r requirements.txt`
5. `py main.py` or `python main.py`
6. Start copying any JP text and see the result being displayed on the app.

## Future Plans:<br/>
1. Add requirements.txt
2. Make settings work
3. Switch GUI framework because TKinter sucks ngl
4. Make a script file to install virtualenv, setup all the requirements in a virtual environment and start app so I don't have to add more clutter to people's pip global packages to their system.
