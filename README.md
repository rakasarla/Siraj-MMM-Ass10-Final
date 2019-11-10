<p align="center"><img src="https://raw.githubusercontent.com/anfederico/Flaskex/master/media/flaskex-logo.png" width="128px"><p>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
![Python](https://img.shields.io/badge/python-v3.6-blue.svg)
![Dependencies](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)
[![GitHub Issues](https://img.shields.io/github/issues/anfederico/flaskex.svg)](https://github.com/anfederico/flaskex/issues)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/ef2f8f65c67a4043a9362fa6fb4f487a)](https://www.codacy.com/app/RDCH106/Flaskex?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=RDCH106/Flaskex&amp;utm_campaign=Badge_Grade)

<br><br>

<p align="center"><img src="https://raw.githubusercontent.com/anfederico/Flaskex/master/media/flaskex-demo.png" width="100%"><p>

## Features
- Encrypted user authorizaton
- Database initialization
- New user signup
- User login/logout
- User settings
- Modern user interface
- Bulma framework
- Limited custom css/js
- Easily customizable

## Setup
``` 
git clone https://github.com/rakasarla/Siraj-MMM-Ass10-Final.git
cd Siraj-MMM-Ass10-Final
pip install -r requirements.txt
python app.py
```

## Contributing
Please take a look at our [contributing](https://github.com/anfederico/Flaskex/blob/master/CONTRIBUTING.md) guidelines if you're interested in helping!


# Siraj-MMM-Ass10-Final
- Date: 10-Nov-2019
- Deployed on Heroku: https://siraj-ass10-final.herokuapp.com/
- Also, due to limitations on Heroku, executing analysis and local laptop
- and uploading results_{ticker}.csv file to display results
- Following ticker result files are currently loaded:
- Tickers: IBM, MSFT, QCOM, FDX, DAL, DIS, FB, AMZN, SPY, GDX, XLF, XOP, EEM and NVDA
- Steps:
- 1. Download tikcet file from finance.yahoo.com for 1 year
- 2. Save this file in ml/code/data/daily_{ticker}.csv
- 3. cd to ml/code
- 4. python run.py --mode test --ticker IBM --weights weights/201911031029-dqn.h5
- 5. make sure ml/code/results/results_{ticker}.csv is created
- 6. Check into github
- 7. Redeploy Heroku (check attached word doc for instructions)

