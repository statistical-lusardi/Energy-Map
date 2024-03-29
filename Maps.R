library(ggplot2)
library(maps)
library(ggmap)
library(mapdata)
library(tidyverse)
library(data.table)
usa<-map_data('usa')
state<-map_data("state")%>%filter(region %in%c("oregon","washington","idaho","california","nevada","montana"))
state

p<-ggplot(data=state, aes(x=long, y=lat,  group=group)) + 
  geom_polygon(color = "white") + 
  guides(fill=FALSE) + 
  # theme(axis.title.x=element_blank(), axis.text.x=element_blank(), axis.ticks.x=element_blank(),
  #       axis.title.y=element_blank(), axis.text.y=element_blank(), axis.ticks.y=element_blank()) + 
  ggtitle('Bonneville Service Territory') + 
  coord_fixed(1.3)

p+geom_point(aes(x=-120,y=44.5),size=7,color="#FF0000")+
  geom_point(aes(x=-122.5,y=44.5),size=5,color="#F80006")+
  geom_point(aes(x=-121,y=45.2),size=5,color="#0000FF")

