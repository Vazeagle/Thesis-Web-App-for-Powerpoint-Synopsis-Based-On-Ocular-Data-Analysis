-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Εξυπηρετητής: 127.0.0.1
-- Χρόνος δημιουργίας: 02 Μαρ 2022 στις 21:33:10
-- Έκδοση διακομιστή: 10.4.22-MariaDB
-- Έκδοση PHP: 8.1.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Βάση δεδομένων: `ez-synopsis`
--

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `coordinates`
--

CREATE TABLE `coordinates` (
  `coordID` bigint(20) NOT NULL,
  `Xcoordinates` float NOT NULL,
  `Υcoordinates` float NOT NULL,
  `Τimestamp` int(11) NOT NULL,
  `collection_date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `ocular_data`
--

CREATE TABLE `ocular_data` (
  `pptx_name` varchar(255) NOT NULL,
  `slide_number` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `coordinateID` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `picture_elements`
--

CREATE TABLE `picture_elements` (
  `pptx_name` varchar(255) NOT NULL,
  `slide_number` int(11) NOT NULL,
  `object_counter` int(11) NOT NULL,
  `pictureXstart` int(11) NOT NULL,
  `pictureYstart` int(11) NOT NULL,
  `pictureWidth` int(11) NOT NULL,
  `pictureHeight` int(11) NOT NULL,
  `objectCategory` varchar(255) NOT NULL,
  `imageLoc` varchar(255) NOT NULL,
  `minTimestamp` int(11) NOT NULL,
  `maxTimestamp` int(11) NOT NULL,
  `occurrenceNum` int(11) NOT NULL,
  `pictureExtensionType` varchar(255) NOT NULL,
  `groupID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Άδειασμα δεδομένων του πίνακα `picture_elements`
--

INSERT INTO `picture_elements` (`pptx_name`, `slide_number`, `object_counter`, `pictureXstart`, `pictureYstart`, `pictureWidth`, `pictureHeight`, `objectCategory`, `imageLoc`, `minTimestamp`, `maxTimestamp`, `occurrenceNum`, `pictureExtensionType`, `groupID`) VALUES
('test2', 1, 1, 114, 645, 421, 277, 'PICTURE', '\\uploads\\test2\\1_1.jpg', 0, 1, 0, 'jpg', NULL),
('test2', 1, 2, 198, 654, 1000, 587, 'PICTURE', '\\uploads\\test2\\1_2.png', 0, 1, 0, 'png', NULL),
('test2', 2, 3, 148, 565, 421, 277, 'PICTURE', '\\uploads\\test2\\2_3.jpg', 0, 1, 0, 'jpg', 0);

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `powerpoint_files`
--

CREATE TABLE `powerpoint_files` (
  `powerpoint_name` varchar(255) NOT NULL,
  `uploader` varchar(255) NOT NULL,
  `upload_date` datetime NOT NULL,
  `save_location` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Άδειασμα δεδομένων του πίνακα `powerpoint_files`
--

INSERT INTO `powerpoint_files` (`powerpoint_name`, `uploader`, `upload_date`, `save_location`) VALUES
('test2', 'vazaios', '2022-03-02 19:36:23', 'uploads\\test2\\test2.pptx');

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `slides`
--

CREATE TABLE `slides` (
  `pptx_name` varchar(255) NOT NULL,
  `slide_number` int(11) NOT NULL,
  `slide_width` int(11) NOT NULL,
  `slide_height` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `textbox_elements`
--

CREATE TABLE `textbox_elements` (
  `pptx_name` varchar(255) NOT NULL,
  `slide_number` int(11) NOT NULL,
  `object_counter` int(11) NOT NULL,
  `textBoxXstart_no_margin` float NOT NULL,
  `textBoxYstart_no_margin` float NOT NULL,
  `textBoxWidth_no_margin` float NOT NULL,
  `textBoxHeight_no_margin` float NOT NULL,
  `objectCategory` varchar(255) NOT NULL,
  `parText` text NOT NULL,
  `minTimestamp` int(11) NOT NULL,
  `maxTimestamp` int(11) NOT NULL,
  `OccurrenceNum` int(11) NOT NULL,
  `eachLineWidth` varchar(255) NOT NULL,
  `lineSpacer` float NOT NULL,
  `lineSizeY` float NOT NULL,
  `fontName` varchar(255) NOT NULL,
  `fontSize` float NOT NULL,
  `marginLeft` float NOT NULL,
  `marginRight` float NOT NULL,
  `marginTop` float NOT NULL,
  `marginBot` float NOT NULL,
  `groupID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Άδειασμα δεδομένων του πίνακα `textbox_elements`
--

INSERT INTO `textbox_elements` (`pptx_name`, `slide_number`, `object_counter`, `textBoxXstart_no_margin`, `textBoxYstart_no_margin`, `textBoxWidth_no_margin`, `textBoxHeight_no_margin`, `objectCategory`, `parText`, `minTimestamp`, `maxTimestamp`, `OccurrenceNum`, `eachLineWidth`, `lineSpacer`, `lineSizeY`, `fontName`, `fontSize`, `marginLeft`, `marginRight`, `marginTop`, `marginBot`, `groupID`) VALUES
('test2', 0, 1, 926.4, 1058.06, 979.2, 109.725, 'TEXT_BOX', 'This isToooooooooooooooooloooooooogg-kkkkkk', 0, 1, 0, '979.1999999999999, 58.2000000000001', 21.945, 43.89, 'arial.ttf', 24, 9.6, 9.6, 0, 0, NULL),
('test2', 0, 2, 926.4, 860.55, 979.2, 43.89, 'TEXT_BOX', 'Sheesh', 0, 1, 0, '159.60000000000002', 21.945, 43.89, 'arial.ttf', 24, 9.6, 9.6, 0, 0, NULL),
('test2', 0, 3, 926.4, 728.88, 979.2, 43.89, 'TEXT_BOX', 'S', 0, 1, 0, '31.92', 21.945, 43.89, 'arial.ttf', 24, 9.6, 9.6, 0, 0, NULL),
('test2', 0, 4, 926.4, 663.045, 979.2, 43.89, 'TEXT_BOX', 'S', 0, 1, 0, '31.92', 21.945, 43.89, 'arial.ttf', 24, 9.6, 9.6, 0, 0, NULL),
('test2', 0, 5, 926.4, 597.21, 979.2, 43.89, 'TEXT_BOX', 'S', 0, 1, 0, '31.92', 21.945, 43.89, 'arial.ttf', 24, 9.6, 9.6, 0, 0, NULL),
('test2', 0, 6, 926.4, 531.375, 979.2, 109.725, 'TEXT_BOX', 'This is a paragrapst Par5 to test what we see in text when the sentence h tecontinues below', 0, 1, 0, '979.1999999999999, 959.94', 21.945, 43.89, 'arial.ttf', 24, 9.6, 9.6, 0, 0, NULL),
('test2', 2, 1, 188.4, 1014.8, 595.2, 43.89, 'TEXT_BOX', 'GROUPING TEST TEXT', 0, 1, 0, '536.6550000000001', 0, 43.89, 'arial.ttf', 24, 9.6, 9.6, 4.8, 4.8, 0),
('test2', 2, 2, 188.4, 970.91, 595.2, 43.89, 'TEXT_BOX', 'Check par2', 0, 1, 0, '241.395', 0, 43.89, 'arial.ttf', 24, 9.6, 9.6, 4.8, 4.8, 0);

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `user`
--

CREATE TABLE `user` (
  `userID` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `temppass` varchar(255) DEFAULT NULL,
  `passreset` tinyint(1) DEFAULT 0,
  `role` enum('admin','user') DEFAULT NULL,
  `verified_user` enum('yes','no') DEFAULT NULL,
  `pptx_settings` tinyint(3) NOT NULL DEFAULT 70,
  `reg_date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Άδειασμα δεδομένων του πίνακα `user`
--

INSERT INTO `user` (`userID`, `username`, `email`, `password`, `temppass`, `passreset`, `role`, `verified_user`, `pptx_settings`, `reg_date`) VALUES
('pbkdf2:sha256:260000$oqGYo8gAMdshMEiY$59af75c5c336362901eeded57548007ae4a02eea90ca0f3e2c62308ae0d3207f', 'vazaios', 'vazeagle@gmail.com', 'pbkdf2:sha256:260000$HysV6UtFb4ziH4ET$216b993c8fb075f448d4229d8fe8d67c1fca3b72dafde82979c430cfcb63a42b', NULL, 0, 'admin', 'yes', 90, '2022-02-12 03:47:16'),
('pbkdf2:sha256:260000$wTuEVuFddpTyAK95$6e53e809ad599bb03e3c3acda1bbc5fcd799aeb12384baa441b8c234aed64605', 'testuser', 'testuser@gmail.com', 'pbkdf2:sha256:260000$h7sbgWhcNRJOfYK8$133238dab03b7ce3802f1c9a5f4193d82afe9e882161e7a31ecd85a191aac774', NULL, 0, 'user', 'no', 70, '2022-03-02 18:14:13');

--
-- Ευρετήρια για άχρηστους πίνακες
--

--
-- Ευρετήρια για πίνακα `coordinates`
--
ALTER TABLE `coordinates`
  ADD PRIMARY KEY (`coordID`);

--
-- Ευρετήρια για πίνακα `ocular_data`
--
ALTER TABLE `ocular_data`
  ADD PRIMARY KEY (`pptx_name`,`slide_number`,`username`,`coordinateID`),
  ADD UNIQUE KEY `coordinateID` (`coordinateID`),
  ADD KEY `ocularDataUsr_to_user` (`username`);

--
-- Ευρετήρια για πίνακα `picture_elements`
--
ALTER TABLE `picture_elements`
  ADD PRIMARY KEY (`pptx_name`,`slide_number`,`object_counter`);

--
-- Ευρετήρια για πίνακα `powerpoint_files`
--
ALTER TABLE `powerpoint_files`
  ADD PRIMARY KEY (`powerpoint_name`),
  ADD KEY `pptxfile_user_uploader` (`uploader`);

--
-- Ευρετήρια για πίνακα `slides`
--
ALTER TABLE `slides`
  ADD PRIMARY KEY (`pptx_name`);

--
-- Ευρετήρια για πίνακα `textbox_elements`
--
ALTER TABLE `textbox_elements`
  ADD PRIMARY KEY (`pptx_name`,`slide_number`,`object_counter`);

--
-- Ευρετήρια για πίνακα `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`userID`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT για άχρηστους πίνακες
--

--
-- AUTO_INCREMENT για πίνακα `coordinates`
--
ALTER TABLE `coordinates`
  MODIFY `coordID` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT για πίνακα `ocular_data`
--
ALTER TABLE `ocular_data`
  MODIFY `coordinateID` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- Περιορισμοί για άχρηστους πίνακες
--

--
-- Περιορισμοί για πίνακα `coordinates`
--
ALTER TABLE `coordinates`
  ADD CONSTRAINT `coordID_to_occularData_coordID` FOREIGN KEY (`coordID`) REFERENCES `ocular_data` (`coordinateID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Περιορισμοί για πίνακα `ocular_data`
--
ALTER TABLE `ocular_data`
  ADD CONSTRAINT `ocularDataUsr_to_user` FOREIGN KEY (`username`) REFERENCES `user` (`username`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `ocularData_pptxName_to_pptxFiles` FOREIGN KEY (`pptx_name`) REFERENCES `powerpoint_files` (`powerpoint_name`) ON DELETE NO ACTION ON UPDATE CASCADE;

--
-- Περιορισμοί για πίνακα `picture_elements`
--
ALTER TABLE `picture_elements`
  ADD CONSTRAINT `picture_pptxName_to_pptxFiles` FOREIGN KEY (`pptx_name`) REFERENCES `powerpoint_files` (`powerpoint_name`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Περιορισμοί για πίνακα `powerpoint_files`
--
ALTER TABLE `powerpoint_files`
  ADD CONSTRAINT `pptxfile_user_uploader` FOREIGN KEY (`uploader`) REFERENCES `user` (`username`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Περιορισμοί για πίνακα `slides`
--
ALTER TABLE `slides`
  ADD CONSTRAINT `pptxfilename_slides` FOREIGN KEY (`pptx_name`) REFERENCES `powerpoint_files` (`powerpoint_name`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Περιορισμοί για πίνακα `textbox_elements`
--
ALTER TABLE `textbox_elements`
  ADD CONSTRAINT `textbox_pptxName_to_pptxFiles` FOREIGN KEY (`pptx_name`) REFERENCES `powerpoint_files` (`powerpoint_name`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
