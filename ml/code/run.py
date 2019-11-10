import pickle
import time
import numpy as np
import argparse
import re
import pandas as pd

from envs import TradingEnv
from agent import DQNAgent
from utils import get_data, get_dates, get_scaler, maybe_make_dir

class Portfolio:
   episode = 0
   value = 0

class Stocks:
   episode = 0
   action = 0
   buyHoldSell = 0
   price = 0
   qty = 0

stockTracker = []
stockPortfolio = []

def addToStockTracker(in_stockTracker):
   stocks = Stocks()
   totalStockBuyQty = 0
   addBuyRecord = False
   for i in range(len(in_stockTracker)):
       # Selling Qty 0 logic
       if in_stockTracker[i].buyHoldSell == 2:
           if in_stockTracker[i].qty > 0:
               stocks.episode = in_stockTracker[i].episode
               stocks.action = in_stockTracker[i].action
               stocks.buyHoldSell = in_stockTracker[i].buyHoldSell
               stocks.stock_date = in_stockTracker[i].stock_date
               stocks.price = in_stockTracker[i].price
               stocks.qty = in_stockTracker[i].qty
               stockTracker.append(stocks)
       elif in_stockTracker[i].buyHoldSell == 0:
           stocks.episode = in_stockTracker[i].episode
           stocks.action = in_stockTracker[i].action
           stocks.buyHoldSell = in_stockTracker[i].buyHoldSell
           stocks.stock_date = in_stockTracker[i].stock_date 
           stocks.price = in_stockTracker[i].price
           totalStockBuyQty += in_stockTracker[i].qty
           addBuyRecord = True

   if addBuyRecord == True:
       stocks.qty = totalStockBuyQty
       stockTracker.append(stocks)




if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-e', '--episode', type=int, default=1000,
                      help='number of episode to run')
  parser.add_argument('-b', '--batch_size', type=int, default=32,
                      help='batch size for experience replay')
  parser.add_argument('-i', '--initial_invest', type=int, default=20000,
                      help='initial investment amount')
  parser.add_argument('-d', '--testingDays', type=int, default=30,
                      help='number of days to trade test')
  parser.add_argument('-t', '--ticker', type=str, default="IBM",
                      help='ticker symbol to analyze')
  parser.add_argument('-m', '--mode', type=str, required=True,
                      help='either "train" or "test"')
  parser.add_argument('-w', '--weights', type=str, help='a trained model weights')
  args = parser.parse_args()

  maybe_make_dir('weights')
  maybe_make_dir('portfolio_val')

  timestamp = time.strftime('%Y%m%d%H%M')
  
  stocks = Stocks()
  portfolio = Portfolio()

  data = np.around(get_data(ticker=args.ticker))
  dataSplit = data.shape[1] - args.testingDays
  train_data = data[:, :dataSplit]
  test_data = data[:, dataSplit:]

  dates = (get_dates(ticker=args.ticker))
  dataesSplit = dates.shape[1] - args.testingDays
  train_dates = dates[:, :dataSplit]
  test_dates = dates[:, dataSplit:]

  env = TradingEnv(stocks, train_data, train_dates, args.initial_invest)
  state_size = env.observation_space.shape
  action_size = env.action_space.n
  agent = DQNAgent(state_size, action_size)
  scaler = get_scaler(env)

  portfolio_value = []

  if args.mode == 'test':
    # remake the env with test data
    env = TradingEnv(stocks, test_data, test_dates, args.initial_invest)
    # load trained weights
    agent.load(args.weights)
    # when test, the timestamp is same as time when weights was trained
    timestamp = re.findall(r'\d{12}', args.weights)[0]

  for e in range(args.episode):
    stocks.episode = e
    state = env.reset()
    state = scaler.transform([state])
    for time in range(env.n_step):
      action = agent.act(state)
      next_state, reward, done, info, v_stockTracker = env.step(action)
      addToStockTracker(v_stockTracker)
      # print("Run -----> Start")
      # for i in range(len(v_stockTracker)):
      #    print("Run -----> episode:{}, action:{}, buyHoldSell:{}, price:{}, qty:{}".format(
      #       v_stockTracker[i].episode, v_stockTracker[i].action, v_stockTracker[i].buyHoldSell,
      #       v_stockTracker[i].price, v_stockTracker[i].qty))			
      # print("Run -----> End")
      next_state = scaler.transform([next_state])
      if args.mode == 'train':
        agent.remember(state, action, reward, next_state, done)
      state = next_state
      if done:
        print("episode: {}/{}, episode end value: {}".format(
          e + 1, args.episode, info['cur_val']))
        portfolio_value.append(info['cur_val']) # append episode end portfolio value
        portfolio = Portfolio()
        portfolio.episode = e # Do you really need "+ 1"?
        portfolio.value = info['cur_val']
        stockPortfolio.append(portfolio)
        break
      if args.mode == 'train' and len(agent.memory) > args.batch_size:
        agent.replay(args.batch_size)
    if args.mode == 'train' and (e + 1) % 10 == 0:  # checkpoint weights
      agent.save('weights/{}-dqn.h5'.format(timestamp))

  # print("Stock Tracker Length:{}".format(str(len(stockTracker))))
  # for i in range(len(stockTracker)):
  #    print("episode:{}, action:{}, buyHoldSell:{}, price:{}, qty:{}".format(
  #           stockTracker[i].episode, stockTracker[i].action, stockTracker[i].buyHoldSell,
  #           stockTracker[i].price, stockTracker[i].qty))

  # Best Episode
  bestEpisode = 0
  bestValue = 0
  for i in range(len(stockPortfolio)):
     if stockPortfolio[i].value > bestValue:
        bestValue = stockPortfolio[i].value
        bestEpisode = stockPortfolio[i].episode
  #    print("episode:{}, value:{}".format(
  #           stockPortfolio[i].episode, stockPortfolio[i].value))			
  print("Best episode:{} and Best value:{}".format(
            bestEpisode, bestValue))

  bestExecution = []
  for i in range(len(stockTracker)):
     if stockTracker[i].episode == bestEpisode:
        stock = Stocks()
        stock.episode = stockTracker[i].episode
        stock.action = stockTracker[i].action
        stock.buyHoldSell = stockTracker[i].buyHoldSell
        stock.stock_date = stockTracker[i].stock_date
        stock.price = stockTracker[i].price
        stock.qty = stockTracker[i].qty
        stock.startValue = args.initial_invest
        stock.endValue = bestValue
        bestExecution.append(stock)

  arr = []
  for i in range(len(bestExecution)):
    arr.append({"episode": bestExecution[i].episode, "action": bestExecution[i].action, 
                "buySell": "buy" if bestExecution[i].buyHoldSell == 0 else "sell",
                "date": bestExecution[i].stock_date, "price": bestExecution[i].price,
                "qty" : bestExecution[i].qty, "startValue": bestExecution[i].startValue,
                "endValue":bestExecution[i].endValue})
    print("episode:{}, action:{}, buyHoldSell:{}, date:{}, price:{}, qty:{}, startValue:{}, endValue:{}".format(
            bestExecution[i].episode, bestExecution[i].action, bestExecution[i].buyHoldSell,
            bestExecution[i].stock_date, bestExecution[i].price, bestExecution[i].qty, 
            bestExecution[i].startValue, bestExecution[i].endValue))
    
  # Convert Array to DataFrame
  df = pd.DataFrame(arr)

  # Write CSV file
  df.to_csv("results/results_" + args.ticker + ".csv")


  # save portfolio value history to disk
  with open('portfolio_val/{}-{}.p'.format(timestamp, args.mode), 'wb') as fp:
    pickle.dump(portfolio_value, fp)
	
  