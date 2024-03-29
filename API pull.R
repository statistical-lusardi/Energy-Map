library(tidyverse)
library(EIAapi)
library(eia)
library(lubridate)
api_url<-"electricity/rto/region-data/data/"
api_key<-"94e8b0bb1fbf7a092e4546c7ba7bdf7f"
eia::eia_set_key(api_key)
range01 <- function(x){(x-min(x))/(max(x)-min(x))}
ramp <- colorRamp(c("red", "blue"))
startdt<-paste0(as.character(date(now())),
       "T",hour(now()-hours(1)))
enddt<-paste0(as.character(date(now())),
              "T",hour(now()))
df<-eia_data(
  dir = "electricity/rto/region-data/data/",
  data = "value",
  start = startdt,
  end=enddt,
  freq = "hourly",
  facets=list(respondent=list("BPAT","BCHA","GCPD","AVRN","IPCO","NWMT",
                              "PACW","PGE","TPWR","PSEI","SCL","GRID",
                              "CHPD","DOPD","AVA","BANC","NEVP","LDWP","CISO"),
              type=list("D"))
)%>%select(period,type,respondent,value)
df$Date<-as.Date(str_split_fixed(df$period,"T",n=2)[,1])
df$HE<-as.numeric(str_split_fixed(df$period,"T",n=2)[,2])

df<-df%>%arrange(Date,HE)%>%select(-period)%>%
  mutate(lagged_hour=as.numeric(lag(value,1)),
         hour=as.numeric(value))%>%na.omit%>%
  group_by(respondent)%>%
  summarise(diff=round((lagged_hour-hour)/hour,2))%>%
  ungroup()%>%
  mutate(colorscale=range01(diff))


df$colors<-rgb(ramp(df$colorscale), maxColorValue = 255)

