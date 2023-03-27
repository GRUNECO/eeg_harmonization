#Pareado proyecto Vero

library(ggplot2)
library(openxlsx)
library(MatchIt)

#Abrir base de datos y asignar factoriales a las variables cualitativas
vero <- read.xlsx ("Prueba.xlsx")
vero$treatall <- factor(vero$treatall)
vero$treatG1 <- factor(vero$treatG1)
vero$sex <- factor(vero$sex)
vero$group <- factor(vero$group)
vero$participant_id <- factor(vero$participant_id)

#Pareado treatall age

veroEDADall <- matchit(treatall~age, data=vero, method = "nearest", ratio=1)
summary(veroEDADall)
#Con ratio=1 y replace=TRUE quedaron 48 controles, perdidos 301 sujetos controles
#Con ratio=1 quedaron 269 controles, perdidos 80 sujetos controles
veroEDADalltreat <- match.data(veroEDADall, group = "treat")
veroEDADallcontrol <- match.data(veroEDADall, group = "control")
veroEDADalltotal <- rbind(veroEDADalltreat,veroEDADallcontrol)
ggplot(veroEDADalltotal, aes(x=treatall, y=age, fill=treatall)) + geom_violin(show.legend = FALSE, alpha=0.5, colour="navyblue", fill = "white", size=1) + geom_boxplot(show.legend = FALSE, alpha=0.5, width=0.2, colour="purple4", fill = "purple4") + stat_summary (fun=median, show.legend = FALSE, geom = "crossbar") + geom_dotplot(binaxis = "y",binwidth = 0.8, stackdir = "center", show.legend = FALSE, colour="black", fill="darkblue")
t.test(veroEDADalltotal$age~veroEDADalltotal$treatall)
#Da estadísticamente significativa
by (veroEDADalltotal$age, veroEDADalltotal$treatall, mean)
by (veroEDADalltotal$age, veroEDADalltotal$treatall, sd)
veroEDADall2 <- matchit(treatall~age, data=vero, method = "nearest", ratio=2)
summary(veroEDADall2)
#Con ratio=2 quedaron 349 controles, perdidos 0 sujetos controles, pero no se haría el match


#Pareado treatG1 age con 1 control

veroEDADG1 <- matchit(treatG1~age, data=vero, method = "nearest", ratio=1)
summary(veroEDADG1)
#Con ratio=1 quedaron 125 controles, perdidos 368 sujetos controles
veroEDADG1treat <- match.data(veroEDADG1, group = "treat")
veroEDADG1control <- match.data(veroEDADG1, group = "control")
veroEDADG1total <- rbind(veroEDADG1treat,veroEDADG1control)
ggplot(veroEDADG1total, aes(x=treatG1, y=age, fill=treatG1)) + geom_violin(show.legend = FALSE, alpha=0.5, colour="navyblue", fill = "white", size=1) + geom_boxplot(show.legend = FALSE, alpha=0.5, width=0.2, colour="purple4", fill = "purple4") + stat_summary (fun=median, show.legend = FALSE, geom = "crossbar") + geom_dotplot(binaxis = "y",binwidth = 0.8, stackdir = "center", show.legend = FALSE, colour="black", fill="darkblue")
t.test(veroEDADG1total$age~veroEDADG1total$treatG1)
write.xlsx(veroEDADG1total, "veroEDADG1total.xlsx")

#Pareado treatG1 age con 2 controles

veroEDADG12 <- matchit(treatG1~age, data=vero, method = "nearest", ratio=2)
summary(veroEDADG12)
#Con ratio=1 quedaron 250 controles, perdidos 243 sujetos controles
veroEDADG12treat <- match.data(veroEDADG12, group = "treat")
veroEDADG12control <- match.data(veroEDADG12, group = "control")
veroEDADG12total <- rbind(veroEDADG12treat,veroEDADG12control)
ggplot(veroEDADG12total, aes(x=treatG1, y=age, fill=treatG1)) + geom_violin(show.legend = FALSE, alpha=0.5, colour="navyblue", fill = "white", size=1) + geom_boxplot(show.legend = FALSE, alpha=0.5, width=0.2, colour="purple4", fill = "purple4") + stat_summary (fun=median, show.legend = FALSE, geom = "crossbar") + geom_dotplot(binaxis = "y",binwidth = 0.8, stackdir = "center", show.legend = FALSE, colour="black", fill="darkblue")
t.test(veroEDADG12total$age~veroEDADG12total$treatG1)

#Pareado treatG1 age + sex con 1 control

veroEDADSEXOG1 <- matchit(treatG1~age+sex, data=vero, method = "nearest", ratio=1)
summary(veroEDADSEXOG1)
#Con ratio=1 quedaron 125 controles, perdidos 368 sujetos controles
veroEDADSEXOG1treat <- match.data(veroEDADSEXOG1, group = "treat")
veroEDADSEXOG1control <- match.data(veroEDADSEXOG1, group = "control")
veroEDADSEXOG1total <- rbind(veroEDADSEXOG1treat,veroEDADSEXOG1control)
ggplot(veroEDADSEXOG1total, aes(x=treatG1, y=age, fill=treatG1)) + geom_violin(show.legend = FALSE, alpha=0.5, colour="navyblue", fill = "white", size=1) + geom_boxplot(show.legend = FALSE, alpha=0.5, width=0.2, colour="purple4", fill = "purple4") + stat_summary (fun=median, show.legend = FALSE, geom = "crossbar") + geom_dotplot(binaxis = "y",binwidth = 0.8, stackdir = "center", show.legend = FALSE, colour="black", fill="darkblue")
t.test(veroEDADSEXOG1total$age~veroEDADSEXOG1total$treatG1)

#Pareado treatG1 age + sex con 2 controles

veroEDADSEXOG12 <- matchit(treatG1~age+sex, data=vero, method = "nearest", ratio=2)
summary(veroEDADSEXOG12)
#Con ratio=1 quedaron 250 controles, perdidos 243 sujetos controles
veroEDADSEXOG12treat <- match.data(veroEDADSEXOG12, group = "treat")
veroEDADSEXOG12control <- match.data(veroEDADSEXOG12, group = "control")
veroEDADSEXOG12total <- rbind(veroEDADSEXOG12treat,veroEDADSEXOG12control)
ggplot(veroEDADSEXOG12total, aes(x=treatG1, y=age, fill=treatG1)) + geom_violin(show.legend = FALSE, alpha=0.5, colour="navyblue", fill = "white", size=1) + geom_boxplot(show.legend = FALSE, alpha=0.5, width=0.2, colour="purple4", fill = "purple4") + stat_summary (fun=median, show.legend = FALSE, geom = "crossbar") + geom_dotplot(binaxis = "y",binwidth = 0.8, stackdir = "center", show.legend = FALSE, colour="black", fill="darkblue")
t.test(veroEDADSEXOG12total$age~veroEDADSEXOG12total$treatG1)

#Para separar G1 y G2 

veroG1 <- subset(vero, group == "G1") 
veroG2 <- subset(vero, group == "G2") 
veroG1G2 <- rbind(veroG1, veroG2)





