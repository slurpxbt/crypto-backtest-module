# crypto-backtest-module
 module for backtesting trading strategies
 
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
 
1. Run <b>load_update_tickers.py</b> this will update existing data in the data folde
     - If you want to add any more tickers to your backtest you need to change line 25 (Binance only)
     - If you want to have only your data delete files in data folder and run script again(It can take some time if you want 1min data <b>[could be up to an 1h for 2 tickers]</b>)
     - Every time you want to update data to the newest you should run this script
     
2. When data is downloaded  open <b>backtest_template.py</b>
   - you can change parameters in lines 19 - 36 and 43 - 45 (don't change other stuff)
   - if you want to add any EMAs or MAs to strategy you should add them to dataframe <b>data</b> anywhere before line 49
   - your strategy should go below line 60
   
3. In the template one strategy is already written so if you have any problems go trough with debbuger to see what the code is doing
4. Although this is really easy to use you should know atleast some python to be able to use it

<b>If you have any question regarding the scripts you can ask me on twitter @slurpxbt</b>


  
 
