library(tidyverse)
library(lubridate)
library(data.table)

file_path <- "D:\\Spring 2021\\Senior Project\\S21_Hess_Rob\\data\\raw\\News events 2007-01-01 thru 2017-09-01 timestamped New York time\\allnews.csv" 

news_data <- read_csv(file_path, col_names = F)

news_data <- news_data %>% rename("date" = X1,
                                  "time" = X2,
                                  "Currency" = X3,
                                  "News_importance" = X4,
                                  "News_description" = X5,
                                  "Actual_value" = X6,
                                  "Predicted_value" = X7,
                                  "Previous_value" = X8,
                                  "Revised_value" = X9,
                                  "result_of_influence" = X10)                                  


View(news_data)

usd_news_data <- news_data %>% filter(Currency == "USD")

View(usd_news_data)

usd_news_data <- news_data %>% filter(Currency == "USD")

usd_FOMC_statements <- usd_news_data %>% filter(News_description == "FOMC Statement")

View(usd_FOMC_statements)

file_path2 <- "D:\\Spring 2021\\Senior Project\\S21_Hess_Rob\\data\\raw\\61,889 news events dated 2007-01-01 thru 2020-11-06 from FF calendar, timestamped New York time\\allnews (rebuilt on 2018-04-07).csv"

news_data <- read_csv(file_path2, col_names = F)

news_data <- news_data %>% rename("date" = X1,
                                  "time" = X2,
                                  "Currency" = X3,
                                  "News_importance" = X4,
                                  "News_description" = X5,
                                  "Actual_value" = X6,
                                  "Predicted_value" = X7,
                                  "Previous_value" = X8,
                                  "Revised_value" = X9,
                                  "result_of_influence" = X10)                                  


View(news_data)

usd_news_data <- news_data %>% filter(Currency == "USD")


usd_FOMC_statements <- usd_news_data %>% filter(News_description == "FOMC Statement")

View(usd_FOMC_statements)

raw_text_path <- "D:/Spring 2021/Senior Project/S21_Hess_Rob/data/raw/Statement_raw_text/"

myFiles <- list.files(path=raw_text_path, pattern="[0-9]+FOMC_statement.txt")

raw_text_data <- data.frame(myFiles) %>%
  rename("file_name" = myFiles) %>% 
  mutate(date = ymd(str_extract(file_name, "\\d+"))) %>%
  mutate(text = map(file_name, function(x) read_file(str_c(raw_text_path,x)))) %>% 
  mutate(text = str_remove_all(text, "(\n)|(\r)"))
  
joined_date <- raw_text_data %>% left_join(usd_FOMC_statements, by = c("date" = "date"))

data_to_write <- joined_date %>% select(date, time, text)
write.csv(data_to_write, "D:\\Spring 2021\\Senior Project\\S21_Hess_Rob\\data\\derived\\raw_text_with_datetime.csv", row.names = F)
