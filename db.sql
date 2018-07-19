-- --------------------------------------------------------
-- Host:                         12player.mysql.database.azure.com
-- Server version:               5.7.21 - MySQL Community Server (GPL)
-- Server OS:                    Win64
-- HeidiSQL Version:             9.5.0.5196
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dumping database structure for mundial
CREATE DATABASE IF NOT EXISTS `mundial` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
USE `mundial`;

-- Dumping structure for table mundial.admins
CREATE TABLE IF NOT EXISTS `admins` (
  `id` tinyint(3) unsigned NOT NULL AUTO_INCREMENT,
  `fname` tinytext NOT NULL,
  `email` varchar(64) NOT NULL,
  `passw` varchar(32) NOT NULL,
  `org_id` tinyint(3) unsigned NOT NULL,
  `city_id` tinyint(3) unsigned NOT NULL,
  `updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `auth_key` varchar(32) CHARACTER SET ascii NOT NULL,
  PRIMARY KEY (`id`),
  KEY `org_id` (`org_id`),
  KEY `city_id` (`city_id`),
  KEY `auth_key` (`auth_key`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

-- Dumping data for table mundial.admins: ~2 rows (approximately)
/*!40000 ALTER TABLE `admins` DISABLE KEYS */;
INSERT INTO `admins` (`id`, `fname`, `email`, `passw`, `org_id`, `city_id`, `updated`, `auth_key`) VALUES
	(1, 'Ssss Kkkk', 'mask@inbox.ru', '3d38f243bec37fa43a0d51dcd60c18c8', 0, 0, '2018-06-22 20:13:20', '47f69cdd8d22e2d35c90350cb596f8dc'),
	(2, 'AS', 'artemsaak@gmail.com', 'e8e2f77fd0b221d3b294a046a1cf48d4', 0, 0, '2018-06-11 15:12:07', '090eec91fc397199bba589872b8b751d');
/*!40000 ALTER TABLE `admins` ENABLE KEYS */;

-- Dumping structure for table mundial.events
CREATE TABLE IF NOT EXISTS `events` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `title` tinytext NOT NULL COMMENT 'название мероприятия',
  `descr` varchar(1024) DEFAULT NULL COMMENT 'краткое описание мероприятия',
  `long_descr` varchar(8192) DEFAULT NULL COMMENT 'длинное описание мероприятия',
  `org_id` tinyint(3) unsigned NOT NULL COMMENT 'id организации',
  `lang_id` tinyint(3) unsigned NOT NULL COMMENT 'id языка',
  `dt` datetime NOT NULL COMMENT 'дата и время мероприятия',
  `status` tinyint(4) NOT NULL DEFAULT '0' COMMENT 'статус мероприятия: -1 отменено, 0 не подтверждено, 1 подтверждено',
  `game_id` tinyint(3) unsigned NOT NULL COMMENT 'id типа мероприятия',
  `city_id` tinyint(3) unsigned NOT NULL COMMENT 'id города мероприятия',
  `addr` tinytext NOT NULL COMMENT 'адрес проведения',
  `map` tinytext COMMENT 'ссылка на карту места проведения',
  `price` smallint(5) unsigned NOT NULL COMMENT 'стоимость',
  `count_min` smallint(5) unsigned NOT NULL COMMENT 'минимальное количество билетов',
  `count_max` smallint(5) unsigned NOT NULL COMMENT 'максимальное количество билетов',
  `count_free` smallint(5) unsigned NOT NULL COMMENT 'количество бесплатных билетов',
  `count_paid` smallint(5) unsigned NOT NULL DEFAULT '0' COMMENT 'количество оплаченных билетов',
  `link` tinytext COMMENT 'ссылка на отчет о мероприятии',
  `upd` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'дата изменения записи',
  `admin_id` tinyint(3) unsigned NOT NULL COMMENT 'id администратора, который добавил мероприятие',
  `img_ext_1` varchar(8) CHARACTER SET ascii DEFAULT NULL COMMENT 'расширение файл с картинкой. если отсутствует, значит нет картинки',
  `img_ext_2` varchar(8) CHARACTER SET ascii DEFAULT NULL COMMENT 'вторая картинка',
  PRIMARY KEY (`id`),
  KEY `org_id` (`org_id`),
  KEY `lang_id` (`lang_id`),
  KEY `city_id` (`city_id`),
  KEY `game_id` (`game_id`),
  KEY `status` (`status`),
  KEY `dt` (`dt`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4;

-- Dumping data for table mundial.events: ~6 rows (approximately)
/*!40000 ALTER TABLE `events` DISABLE KEYS */;
INSERT INTO `events` (`id`, `title`, `descr`, `long_descr`, `org_id`, `lang_id`, `dt`, `status`, `game_id`, `city_id`, `addr`, `map`, `price`, `count_min`, `count_max`, `count_free`, `count_paid`, `link`, `upd`, `admin_id`, `img_ext_1`, `img_ext_2`) VALUES
	(1, 'Космическое приключение 1', 'Space Quest I: The Sarien Encounter (рус. Космическое приключение I: Столкновение с сариенами) — первая часть приключенческой саги Space Quest.происходят невероятные истории, дающие ему шанс спасти галактику.', 'История начинается на звездолёте Arcada, на борту которого находится Звёздный Генератор. Постройка этого генератора и была целью миссии звездолёта. Экипаж празднует победу, возвращаясь на родную планету Ксенон. Но никто не замечает, что странное космическое судно приближается сзади.\r\n\r\nПиратский космический корабль Deltaur пристыковался к «Аркаде». Весь экипаж был убит, Звёздный Генератор украден. В живых остался только один — уборщик Роджер Вилко. Он же главный герой этой игры.\r\n\r\nЦель игры — вернуть Звёздный Генератор людям, пройдя все преграды и опасности.\r\n\r\nС помощью этого генератора инопланетяне собрались уничтожить планету Ксенон и захватить власть над всей Галактикой.', 2, 1, '2018-06-25 13:00:00', 0, 3, 2, 'Марсово поле, 5', 'https://www.google.ru/maps/place/Marsovo+Pole,+5,+Sankt-Peterburg,+191186/@59.9429602,30.3279409,17z/data=!4m5!3m4!1s0x4696310dbe200ad7:0x502448758c7a1a!8m2!3d59.942713!4d30.328649', 900, 15, 50, 0, 1, '', '2018-06-21 17:28:15', 1, 'jpg', 'jpg'),
	(2, 'Космическое приключение 2', 'Space Quest II: Vohaul’s Revenge — приключенческая игра, разработанная Sierra Entertainment. Дата релиза — 14 ноября 1987 года. Сиквел первой части серии Space Quest — The Sarien Encounter.', 'Сначала игроку в комическом стиле кратко пересказывают сюжет первой части, где уборщик Роджер Вилко стал героем планеты Ксенон. Также в этом вступлении игрок узнаёт, кто был главным негодяем (командующий атакой сариенов на корабль «Аркада» в предыдущей части игры) в истории несостоявшегося разрушения Ксенона — безумного учёного Слажда Вохаула — и как он сошёл с ума. Далее начинается сюжет второй части.\r\n\r\nРоджер Вилко, благодаря своему статусу героя Ксенона, был отправлен на Ксенонскую Орбитальную Станцию 4 и получил там должность главного (и единственного) уборщика. Вскорости наступившую идиллию нарушает Сладж Вохаул, похищая Роджера…\r\n\r\nГлавному герою вскоре везёт — корабль с ним на борту терпит аварийную посадку на планете Лабион и Роджеру удаётся сбежать из плена. Пройдя через опасные джунгли планеты Вилко добирается до базы-астероида Сладжа Вохаула, чтобы помешать исполнению его второго плана по уничтожению жизни в галактике. На этот раз с помощью клонированных страховых агентов.\r\n\r\nВ итоге Роджер взрывает базу-астероид и благополучно драпает оттуда перед взрывом на космическом челноке, однако перед этим ему пришлось погрузиться в криосон, что стало завязкой к Space Quest III: The Pirates of Pestulon.', 2, 1, '2018-06-25 19:00:00', 0, 3, 1, 'Красная площадь, 3', 'https://www.google.ru/maps/place/Krasnaya+ploshad,+3,+Moskva,+101000/data=!4m2!3m1!1s0x46b54a5a1c716c07:0x72f16fa7fabe17ae?sa=X&ved=0ahUKEwiJ59TprOXbAhWGiCwKHcG0C5YQ8gEIKDAA', 900, 15, 60, 0, 2, '', '2018-06-21 18:13:00', 1, 'jpg', 'jpg'),
	(3, 'Space Quest III', 'Space Quest III: The Pirates of Pestulon is a 1989 graphic adventure game by Sierra On-Line, and the third game in the Space Quest series.', 'Roger Wilco\'s escape pod from the end of Space Quest II is floating in space until it is picked up by an automated garbage freighter. Finding a derelict spaceship amongst the freighter\'s garbage, Roger sets out to repair the Aluminum Mallard and leave the scow.\r\n\r\nRoger visits a variety of locations, including a fast food restaurant called Monolith Burger and a desert planet called Phleebhut. At the latter, he encounters trouble, as Arnoid the Annihilator (an Arnold Schwarzenegger-like android terminator) persecutes him for not paying for a whistle acquired in Space Quest II (either a "continuity" error, or a spoof, since the order form for the whistle clearly states it was supposed to be free). From information he picks up there and at Monolith Burger, Roger eventually uncovers the sinister activities of a video game company known as ScumSoft, run by the "Pirates of Pestulon".\r\n\r\nPestulon, a small moon of the volcanic planet Ortega, is covered in soft, moss-like vegetation, and dotted with twisted tree-like growths throughout. Elmo Pug, the CEO of ScumSoft, has abducted the Two Guys from Andromeda and is forcing them to design awful games.\r\n\r\nRoger manages to sneak into the supposedly impregnable ScumSoft building and rescue the two programmers. He is discovered, and must battle Pug in a game that combines giant Mecha-style combat with Rock \'Em Sock \'Em Robots. After winning, Roger and the Two Guys escape. In the game\'s conclusion, Roger delivers the two game designers to Sierra On-Line\'s president, Ken Williams, on Earth.', 3, 2, '2018-06-26 14:00:00', 0, 1, 9, 'нижегородская ярмарка', 'https://www.google.ru/maps/place/Nizhegorodskaya+Yarmarka/@55.767705,37.6016673,17z/data=!3m1!4b1!4m5!3m4!1s0x46b54a3f5bf9f695:0x9b6141929f080992!8m2!3d55.767705!4d37.603856', 900, 15, 65, 0, 0, '', '2018-06-21 18:36:52', 1, 'jpg', 'jpg'),
	(4, 'Space Quest IV', 'Space Quest IV: Roger Wilco and the Time Rippers is a 1991 graphic adventure game by Sierra On-Line. ', 'Space Quest IV: Roger Wilco and the Time Rippers is a 1991 graphic adventure game by Sierra On-Line. It was released on floppy disks on March 4, 1991, and released on CD-ROM in December 1992 with full speech support and featuring Laugh-In announcer Gary Owens as the voice of the narrator. It featured 256-color hand painted graphics and a fully mouse-driven interface. It was one of the first games to use motion capture animation. The game cost over US$1,000,000 to produce and sold more than its three predecessors combined. An Atari ST version was announced via Sierra Online\'s magazine, Sierra News Magazine, but was later canceled.', 3, 2, '2018-06-26 22:00:00', 0, 1, 8, 'ул. Льва Толстого, 131, отель Хилтон', 'https://www.google.ru/maps/place/Hampton+by+Hilton+Samara/@53.2605796,49.9179003,10z/data=!4m17!1m9!2m8!1sHotels!3m6!1sHotels!2sSamara,+Samara+Oblast!3s0x416618e22bd879d3:0xba95cda9bb3a030b!4m2!1d50.2212463!2d53.2415041!3m6!1s0x41661e72a09ecfb9:0x95b45a3b', 900, 3, 90, 0, 0, '', '2018-06-21 18:47:27', 1, 'jpg', 'jpg'),
	(5, 'Space Quest V', 'Space Quest V : La Mutation suivante est un jeu vidéo d\'aventure sorti en 1993 sous DOS. Le jeu a été développé par Dynamix et édité par Sierra. Il fait partie de la série des Space Quest.', 'Space Quest V : La Mutation suivante est un jeu vidéo d\'aventure sorti en 1993 sous DOS. Le jeu a été développé par Dynamix et édité par Sierra. Il fait partie de la série des Space Quest.\r\n\r\nDepuis ses mésaventures avec les Égorgeurs du Temps dans Space Quest IV, Roger a intégré une université spatiale afin d\'évoluer dans son emploi. Une fois son diplôme obtenu (en trichant à l\'examen), il devient... Responsable d\'un vaisseau poubelle chargé de récupérer les déchets aux quatre coins de la galaxie.\r\n\r\nSes pérégrinations sont pourtant vite troublées par une étrange androïde tueuse à gages, chargée de l\'éliminer...', 4, 6, '2018-06-27 16:00:00', 0, 3, 11, 'La gare de Kaliningrad', 'https://www.google.ru/maps?newwindow=1&q=%D0%BA%D0%B0%D0%BB%D0%B8%D0%BD%D0%B8%D0%BD%D0%B3%D1%80%D0%B0%D0%B4%D1%81%D0%BA%D0%B8%D0%B9+%D0%B2%D0%BE%D0%BA%D0%B7%D0%B0%D0%BB&um=1&ie=UTF-8&sa=X&ved=0ahUKEwjbkdfHt-XbAhXJDywKHcDvAdMQ_AUICigB', 950, 5, 75, 1, 0, '', '2018-06-21 19:01:17', 1, 'jpg', 'jpg'),
	(6, 'Space Quest VI', 'Space Quest VI: The Spinal Frontier est un jeu d\'aventure développé et publié par Sierra On-Line en mars 1995 sur PC et Macintosh. ', 'Space Quest VI: The Spinal Frontier est un jeu d\'aventure développé et publié par Sierra On-Line en mars 1995 sur PC et Macintosh. C’est le sixième épisode de la série Space Quest se déroulant dans un univers de science-fiction humoristique. Le jeu a été conçu par Josh Mandel et Scott Murphy1 et est basé sur le moteur Sierra’s Creative Interpreter permettant au joueur de contrôler son personnage via une interface en pointer-et-cliquer.', 1, 6, '2018-06-27 22:00:00', 0, 3, 3, 'Stade olympique Ficht', 'https://www.google.ru/maps?q=%D1%81%D1%82%D0%B0%D0%B4%D0%B8%D0%BE%D0%BD+%D1%84%D0%B8%D1%88%D1%82&um=1&ie=UTF-8&sa=X&ved=0ahUKEwjEqJfdueXbAhWCZCwKHXrJDYMQ_AUICygC', 990, 3, 30, 1, 0, '', '2018-06-21 19:08:54', 1, 'png', 'png');
/*!40000 ALTER TABLE `events` ENABLE KEYS */;

-- Dumping structure for table mundial.states
CREATE TABLE IF NOT EXISTS `states` (
  `tg_id` bigint(20) unsigned NOT NULL COMMENT 'id Телеграм-юзера',
  `dt` date NOT NULL COMMENT 'дата, которую указал пользователь',
  `city_id` tinyint(3) unsigned NOT NULL COMMENT 'id города проведения',
  KEY `city_id` (`city_id`),
  KEY `d` (`dt`),
  KEY `tg_id` (`tg_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dumping data for table mundial.states: ~2 rows (approximately)
/*!40000 ALTER TABLE `states` DISABLE KEYS */;
INSERT INTO `states` (`tg_id`, `dt`, `city_id`) VALUES
	(1000, '2018-06-23', 8),
	(1000, '2018-06-22', 1);
/*!40000 ALTER TABLE `states` ENABLE KEYS */;

-- Dumping structure for table mundial.tg_admins
CREATE TABLE IF NOT EXISTS `tg_admins` (
  `id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `uname` varchar(32) NOT NULL,
  `org_id` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `city_id` tinyint(3) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `org_id` (`org_id`),
  KEY `city_id` (`city_id`)
) ENGINE=InnoDB AUTO_INCREMENT=194 DEFAULT CHARSET=utf8mb4;

-- Dumping data for table mundial.tg_admins: ~32 rows (approximately)
/*!40000 ALTER TABLE `tg_admins` DISABLE KEYS */;
INSERT INTO `tg_admins` (`id`, `uname`, `org_id`, `city_id`) VALUES
	(162, 'qqq', 1, 4),
	(163, 'www', 1, 4),
	(164, 'eee', 1, 4),
	(165, 'rrr', 1, 10),
	(166, 'ttt', 1, 10),
	(167, 'yyy', 1, 10),
	(168, 'uuu', 1, 6),
	(169, 'iii', 1, 6),
	(170, 'ooo', 1, 6),
	(171, 'sss', 1, 11),
	(172, 'ddd', 1, 11),
	(173, 'fff', 1, 11),
	(174, 'ggg', 1, 1),
	(175, 'hhh', 1, 1),
	(176, 'jjj', 1, 1),
	(177, 'kkk', 1, 9),
	(178, 'lll', 1, 9),
	(179, 'zzz', 1, 9),
	(180, 'xxx', 1, 5),
	(181, 'vvv', 1, 5),
	(182, 'bbb', 1, 8),
	(183, 'nnn', 1, 8),
	(184, 'mmm', 1, 8),
	(185, '111', 1, 2),
	(186, '222', 1, 2),
	(187, '333', 1, 2),
	(188, '444', 1, 7),
	(189, '555', 1, 7),
	(190, '666', 1, 7),
	(191, '777', 1, 3),
	(192, '888', 1, 3),
	(193, '999', 1, 3);
/*!40000 ALTER TABLE `tg_admins` ENABLE KEYS */;

-- Dumping structure for table mundial.tg_users
CREATE TABLE IF NOT EXISTS `tg_users` (
  `id` bigint(20) unsigned NOT NULL COMMENT 'id Телеграма',
  `uname` varchar(64) NOT NULL COMMENT 'имя пользователя Телеграма',
  `fname` tinytext NOT NULL COMMENT 'Полное имя',
  `langs` tinyint(3) unsigned NOT NULL COMMENT 'Битовая маска языков мероприятий',
  `lang_id` tinyint(3) unsigned NOT NULL COMMENT 'id языка интерфейса',
  `city_def` tinyint(3) unsigned NOT NULL DEFAULT '1' COMMENT 'Город по-умолчанию',
  `src` varchar(20) DEFAULT NULL COMMENT 'Источник посещения',
  `ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'дата и время создания',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dumping data for table mundial.tg_users: ~9 rows (approximately)
/*!40000 ALTER TABLE `tg_users` DISABLE KEYS */;
INSERT INTO `tg_users` (`id`, `uname`, `fname`, `langs`, `lang_id`, `city_def`, `src`, `ts`) VALUES
	(1000, 'rwilco', 'Roger Wilco', 11, 1, 1, 'url', '2018-06-21 22:51:44'),
	(147797200, '', 'Ivan Kivinov', 0, 0, 1, '', '2018-06-23 06:26:03'),
	(212921194, '', 'Andrew K', 0, 0, 1, '', '2018-06-20 19:55:05'),
	(233737364, 'artemsaak', 'Artem Saakyan', 16, 2, 10, 'landing', '2018-06-20 17:25:29'),
	(263324891, 'mmcdonald', 'Melissa McDonald', 0, 0, 1, '', '2018-06-26 17:28:02'),
	(388113617, '', 'Sasha Krasnov', 63, 1, 1, NULL, '2018-06-12 20:04:41'),
	(442017607, 'Alexxlxxl', 'AleXXL', 0, 0, 1, '', '2018-06-26 13:34:20'),
	(458329310, '', 'Анастасия', 20, 0, 1, '', '2018-06-17 20:43:53'),
	(503955264, '', 'Амбарцум Кесьян', 34, 0, 1, '', '2018-06-18 13:15:27'),
	(511621312, 'mkatkap', 'Scaner', 0, 0, 1, '', '2018-06-27 20:51:00');
/*!40000 ALTER TABLE `tg_users` ENABLE KEYS */;

-- Dumping structure for table mundial.tickets
CREATE TABLE IF NOT EXISTS `tickets` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id билета',
  `event_id` int(10) unsigned NOT NULL COMMENT 'id события',
  `tg_id` bigint(10) unsigned NOT NULL COMMENT 'id Телеграм-юзера',
  `t_buy` varchar(40) CHARACTER SET ascii DEFAULT NULL COMMENT 'транзакция покупки',
  `t_refund` varchar(40) CHARACTER SET ascii DEFAULT NULL COMMENT 'транзакция возврата',
  `status` tinyint(4) NOT NULL DEFAULT '0' COMMENT 'статус билета. 0 - нормальный билет, 1 - погашенный, -1 возврат',
  `t_code` varchar(20) CHARACTER SET ascii DEFAULT NULL COMMENT 'внутренний код билета',
  `ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'дата и время добавления строки',
  PRIMARY KEY (`id`),
  UNIQUE KEY `t_buy` (`t_buy`),
  UNIQUE KEY `t_refund` (`t_refund`),
  KEY `event_id` (`event_id`),
  KEY `user_id` (`tg_id`),
  KEY `code` (`t_code`),
  KEY `status` (`status`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4;

-- Dumping data for table mundial.tickets: ~1 rows (approximately)
/*!40000 ALTER TABLE `tickets` DISABLE KEYS */;
INSERT INTO `tickets` (`id`, `event_id`, `tg_id`, `t_buy`, `t_refund`, `status`, `t_code`, `ts`) VALUES
	(26, 2, 1000, '1234567890', '11111111', -1, '74284-68825', '2018-06-22 11:51:07'),
	(27, 1, 233737364, 'trans1', NULL, 0, '19423-36175', '2018-06-24 18:57:42');
/*!40000 ALTER TABLE `tickets` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
