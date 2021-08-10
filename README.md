# crypto-backtest-module
 module for backtesting trading strategies based on candle data
 
 <h3>Instructions how to use the script</h3>
 
 <p>Required packages:<p>
 <ul>
   <li>python-binance</li>
   <li>pandas</li>
   <li>time</li>
   <li>matplotlib</li>
   <li>numpy</li>
   <li><b>If any other are missing just pip install them</b></li>
 </ul>
 
 <p>How to run backtest template:</p>
 
1. Run <b>load_update_tickers.py</b> this will update existing data in the data folder
     - At the end of this file species ticker you want data for and timeframes
     - If you want to have only your data delete files in data folder and run script again(It can take some time if you want 1min data <b>[could be up to an 1h for 2 tickers]</b>)
     - Every time you want to update data to the newest you should run this script
     
2. When data is downloaded  open <b>backtest_template.py</b>
   - in this file you can test strategies
   
3. Although this is really easy to use you should know atleast some python to be able to use it

<b>If you have any question regarding the scripts you can ask me on twitter @slurpxbt</b>


  
 
