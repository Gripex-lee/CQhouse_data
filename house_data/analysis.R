library(RMySQL)
library(mice)

# �������ݿ�'cqhouse'
con1=dbConnect(RMySQL::MySQL(),
               dbname='cqhouse',
               username='root',
               password='liwenwu.610',
               host
               ='localhost')
# ���ñ�������������
dbSendQuery(con1,"SET NAMES gbk")

# ��'cqhouse'��'house_data'�е�������
res = dbSendQuery(con1,"select * from house_data;")
mydata = dbFetch(res,n=-1)

head(mydata)
# �޸�����
# fix(mydata)
colnames(mydata) = c("id","price","total_price","bedroom","living_room","floor","toward",
                      "type","size","build_year","building_type","elector","Community_name","location")
attach(mydata)

mydata$id = as.integer(mydata$id)
mydata$price = as.numeric(mydata$price)
mydata$total_price = as.numeric(mydata$total_price)
mydata$bedroom = as.integer(mydata$bedroom)
mydata$living_room = as.integer(mydata$living_room)
mydata$floor = as.integer(mydata$floor)
mydata$size = as.numeric(mydata$size)
mydata$build_year = as.integer(mydata$build_year)
mydata$toward = as.factor(mydata$toward)
mydata$type = as.factor(mydata$type)
mydata$building_type = as.factor(mydata$building_type)
mydata$elector = as.factor(mydata$elector)
mydata$location = as.factor(mydata$location)

data = mydata[,names(mydata) %in% c("id","price","bedroom","living_room","floor","size",
                                    "build_year","type","building_type","elector","location")]
data$elector[which(data$elector == "��������")] = NA
data$type[which(data$type == "����")] = NA

summary(data)
# �鿴ȱʧֵ
md.pattern(data)
library(VIM)
aggr_plot <- aggr(data, col=c('navyblue','red'), 
                  numbers=TRUE, 
                  sortVars=TRUE, 
                  labels=names(data[,-1]), 
                  cex.axis=.7, 
                  gap=3, 
                  ylab=c("����ȱʧģʽֱ��ͼ","ģʽ"))

# ����ȱʧֵ
# build_year��ȱʧֵ�����ɭ�֣�
mice_mod <- mice(data[, !names(data) %in% c('id','bedroom','living_room','elector','price','type')],
                 method='rf')  #rfΪrandomForest
mice_output <- complete(mice_mod)
data$build_year <- mice_output$build_year

# elector��ȱʧֵ ����ڲ岹KNN
require(DMwR)
knnOutput <- knnImputation(data[,!names(data) %in% c('id','price','bedroom','living_room','type','size','building_type')],meth = "weighAvg") 
data$elector <- knnOutput$elector

# type��ȱʧֵ
knnOutput <- knnImputation(data[,!names(data) %in% c('id','price','bedroom','living_room','size','elector')],meth = "weighAvg") 
data$type <- knnOutput$type

md.pattern(data)

str(data[,-1])
summary(data[,-1])
# priceֱ��ͼ
ggplot(data,aes(x=price))+geom_histogram(binwidth = 200, fill = "blue", colour = "grey")

attach(data)
library(ggplot2)
library(corrplot)
# �۸���ڵ�����װ��״�������µ�����ͼ
ggplot(data,aes(x=elector,y=price))+
  geom_boxplot()+
  facet_wrap(~type,scales = "free")

# �۸����װ��״��
ggplot(data,aes(x=type,y=price))+geom_boxplot()

# �۸���ڵص�
ggplot(data,aes(x=location,y=price))+geom_boxplot()

corr <- cor(data[,c('price','bedroom','living_room','floor','size','build_year')])
corrplot(corr = corr,order="AOE",type="upper",tl.pos="tp")
corrplot(corr = corr, add=TRUE,type="lower", method="number",order="AOE", col="black",diag=FALSE,tl.pos="n", cl.pos="n")


# ģ��1
lm1=lm(price~bedroom+living_room+floor+type+size+build_year+building_type+elector+location,data)
summary(lm1)
anova(lm1)

# ģ��2
lm2=lm(price~bedroom+living_room+type+size+build_year+elector+location,data)
summary(lm2)
anova(lm2)

detach(data)