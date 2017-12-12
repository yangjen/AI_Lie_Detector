DROP DATABASE IF EXISTS P5BA;
CREATE DATABASE P5BA;
USE P5BA;

CREATE TABLE Question(
   questionID  INT auto_increment, 
   question VARCHAR(200),
   PRIMARY KEY (questionID));
   
   CREATE TABLE Session_question(
   sessionQuesID INT,
   sessionID INT,
   questionID INT,
   sequence INT,
   pLabel INT,
   tLabel INT,
   PRIMARY KEY (sessionQuesID)
   );
   
   create table Session(
    sessionID INT ,
    sessionTimestamp long,
    PRIMARY KEY (sessionID)
    );
   
   CREATE TABLE Gaze(
   gazeID INT auto_increment,
   sessionQuesID INT,
   gazeTimestamp long,
   x VARCHAR(40),
   y VARCHAR(40),
   confidence VARCHAR(40),
   PRIMARY KEY (gazeID)
   );
   
create table LogEvent(
	eventID  INT auto_increment, 
	sessionID INT,
    eventTimestamp long,
    logEvent varchar(50),
    PRIMARY KEY (eventID)
    );
    
create table Expression(
    expressionID INT auto_increment,
    sessionQuesID INT,
    expTimestamp long,
    gender varchar(10),
    glasses varchar(10),
    age varchar(10),
    ethnicity varchar(10),
    joy int,
    sadness int,
    disgust int,
    contempt int,
    anger int,
    fear int,
    surprise int,
    valence int,
    engagement int,
    smile int,
    innerBrowRaise int,
    browRaise int,
    browFurrow int,
    noseWrinkle int,
    upperLipRaise int,
    lipCornerDepressor int,
    chinRaise int,
    lipPucker int,
    lipPress int,
    lipSuck int,
    mouthOpen int,
    smirk int,
    eyeClosure int,
    attention int,
    lidTighten int,
    jawDrop int,
    dimpler int,
    eyeWiden int,
    cheekRaise int,
    lipStretch int,
    PRIMARY KEY (expressionID)
    );
    
    
INSERT INTO `P5BA`.`Session_question` (`sessionQuesID`, `sessionID`, `questionID`, `sequence`, `pLabel`) VALUES ('0', '0', '0', '0', '0');
INSERT INTO `P5BA`.`Session` (`sessionID`) VALUES ('0');

    
INSERT INTO `P5BA`.`Question` (`questionID`, `question`) VALUES ('1', 'Have you ever peed when you are in a shower/pool?');
INSERT INTO `P5BA`.`Question` (`questionID`, `question`) VALUES ('2', 'Do you pick your nose?');
INSERT INTO `P5BA`.`Question` (`questionID`, `question`) VALUES ('3', 'Do you have a secret crash?');
INSERT INTO `P5BA`.`Question` (`questionID`, `question`) VALUES ('4', 'Have you watched a porn within the last week?');
INSERT INTO `P5BA`.`Question` (`questionID`, `question`) VALUES ('5', 'Have you ever shoplifted?');
INSERT INTO `P5BA`.`Question` (`questionID`, `question`) VALUES ('6', 'How would you rate your looks on a scale of 1 to 10?');
INSERT INTO `P5BA`.`Question` (`questionID`, `question`) VALUES ('7', 'How many guys have you dated so far?');
INSERT INTO `P5BA`.`Question` (`questionID`, `question`) VALUES ('8', 'Have you cheated on your boyfriend/girlfriend before?');
INSERT INTO `P5BA`.`Question` (`questionID`, `question`) VALUES ('9', 'Have you ever done drunk driving?');
INSERT INTO `P5BA`.`Question` (`questionID`, `question`) VALUES ('10', 'Have you ever farted in an elevator?');
INSERT INTO `P5BA`.`Question` (`questionID`, `question`) VALUES ('11', 'Have you ever practiced kissing in a mirror?');
INSERT INTO `P5BA`.`Question` (`questionID`, `question`) VALUES ('12', 'Do you snore?');
INSERT INTO `P5BA`.`Question` (`questionID`, `question`) VALUES ('13', 'Do you think you’ll marry your current girlfriend/boyfriend?');
INSERT INTO `P5BA`.`Question` (`questionID`, `question`) VALUES ('14', 'If you were allowed to marry more than one person, would you?');
INSERT INTO `P5BA`.`Question` (`questionID`, `question`) VALUES ('15', 'If someone offered you 1 million dollars to break up with your girlfriend/boyfriend, would you do it?');
INSERT INTO `P5BA`.`Question` (`questionID`, `question`) VALUES ('16', 'Have you ever thought about cheating on your partner?');
INSERT INTO `P5BA`.`Question` (`questionID`, `question`) VALUES ('17', 'If you ran out of toilet paper, would you consider wiping with the empty roll?');
INSERT INTO `P5BA`.`Question` (`questionID`, `question`) VALUES ('18', 'Have you ever had a crush on a friend’s girlfriend/boyfriend?');
INSERT INTO `P5BA`.`Question` (`questionID`, `question`) VALUES ('19', 'Is there a person that you are always jealous of?');
INSERT INTO `P5BA`.`Question` (`questionID`, `question`) VALUES ('20', 'If you had to choose between dating someone ugly who was good in bed or dating someone hot who was bad in bed, which would you choose?');
INSERT INTO `P5BA`.`Question` (`questionID`, `question`) VALUES ('21', 'If you had to choose between being poor and smart or being rich and dumb, what would you choose?');
INSERT INTO `P5BA`.`Question` (`questionID`, `question`) VALUES ('22', 'How was your first job?');
INSERT INTO `P5BA`.`Question` (`questionID`, `question`) VALUES ('23', 'Can you explain how amazing you find Machine Learning module?');