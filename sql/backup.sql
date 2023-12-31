PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE Questions (
    QuestionID INTEGER PRIMARY KEY,
    QuestionText TEXT
);
INSERT INTO Questions VALUES(1,'What is the best source for information about securing a physical asset''s BIOS?');
INSERT INTO Questions VALUES(2,'Which of the following roles is responsible for creating cloud components and the testing and validation of services?');
INSERT INTO Questions VALUES(3,'Which of the following is not a component of contractual PII?');
INSERT INTO Questions VALUES(4,'Which of the following concepts refers to a cloud customer paying only for the resources and offerings they use within a cloud environment, and only for the duration that they are consuming them?');
INSERT INTO Questions VALUES(5,'Which of the following roles involves testing, monitoring, and securing cloud services for an organization?');
INSERT INTO Questions VALUES(6,'What is the only data format permitted with the SOAP API?');
INSERT INTO Questions VALUES(7,'Which data formats are most commonly used with the REST API?');
INSERT INTO Questions VALUES(8,'Which of the following threat types involves an application that does not validate authorization for portions of itself after the initial checks?');
INSERT INTO Questions VALUES(9,'Which of the following roles involves overseeing billing, purchasing, and requesting audit reports for an organization within a cloud environment?');
INSERT INTO Questions VALUES(10,'What is the biggest concern with hosting a key management system outside of the cloud environment?');
INSERT INTO Questions VALUES(11,'Which of the following approaches would NOT be considered sufficient to meet the requirements of secure data destruction within a cloud environment?');
INSERT INTO Questions VALUES(12,'Which of the following cloud aspects complicates eDiscovery?');
INSERT INTO Questions VALUES(13,'What does the management plane typically utilize to perform administrative functions on the hypervisors that it has access to?');
INSERT INTO Questions VALUES(14,'What is a serious complication an organization faces from the perspective of compliance with international operations?');
INSERT INTO Questions VALUES(15,'Which networking concept in a cloud environment allows for network segregation and isolation of IP spaces?');
INSERT INTO Questions VALUES(16,'Which of the following standards primarily pertains to cabling designs and setups in a data center?');
INSERT INTO Questions VALUES(17,'Which of the following publishes the most commonly used standard for data center design in regard to tiers and topologies?');
INSERT INTO Questions VALUES(18,'What type of segregation and separation of resources is needed within a cloud environment for multitenancy purposes versus a traditional data center model?');
INSERT INTO Questions VALUES(19,'Which United States law is focused on data related to health records and privacy?');
INSERT INTO Questions VALUES(20,'What is used for local, physical access to hardware within a data center?');
INSERT INTO Questions VALUES(21,'Within an Infrastructure as a Service model, which of the following would NOT be a measured service?');
INSERT INTO Questions VALUES(22,'Which of the following is NOT a criterion for data within the scope of eDiscovery?');
INSERT INTO Questions VALUES(23,'Which United States law is focused on accounting and financial practices of organizations?');
INSERT INTO Questions VALUES(24,'What type of masking strategy involves making a separate and distinct copy of data with masking in place?');
INSERT INTO Questions VALUES(25,'Which of the following storage types is most closely associated with a database-type storage implementation?');
INSERT INTO Questions VALUES(26,'Which of the following roles is responsible for overseeing customer relationships and the processing of financial transactions?');
INSERT INTO Questions VALUES(27,'Which protocol does the REST API depend on?');
INSERT INTO Questions VALUES(28,'Which United States program was designed to enable organizations to bridge the gap between privacy laws and requirements of the United States and the European Union?');
INSERT INTO Questions VALUES(29,'What is the biggest benefit to leasing space in a data center versus building or maintain your own?');
INSERT INTO Questions VALUES(30,'Which of the following security measures done at the network layer in a traditional data center are also applicable to a cloud environment?');
INSERT INTO Questions VALUES(31,'Which aspect of cloud computing will be most negatively impacted by vendor lock-in?');
INSERT INTO Questions VALUES(32,'Which of the following APIs are most commonly used within a cloud environment?');
INSERT INTO Questions VALUES(33,'Which of the following attempts to establish an international standard for eDiscovery processes and best practices?');
INSERT INTO Questions VALUES(34,'Which of the following roles is responsible for obtaining new customers and securing contracts and agreements?');
INSERT INTO Questions VALUES(35,'Which term relates to the application of scientific methods and practices to evidence?');
INSERT INTO Questions VALUES(36,'Which of the following roles involves the provisioning and delivery of cloud services?');
INSERT INTO Questions VALUES(37,'What is the primary reason that makes resolving jurisdictional conflicts complicated?');
INSERT INTO Questions VALUES(38,'GAAPs are created and maintained by which organization?');
INSERT INTO Questions VALUES(39,'Which of the following roles is responsible for preparing systems for the cloud, administering and monitoring services, and managing inventory and assets?');
INSERT INTO Questions VALUES(40,'Which protocol allows a system to use block-level storage as if it was a SAN, but over TCP network traffic instead?');
INSERT INTO Questions VALUES(41,'Which of the cloud deployment models is used by popular services such as iCloud, Dropbox, and OneDrive?');
INSERT INTO Questions VALUES(42,'Why does a Type 2 hypervisor typically offer less security control than a Type 1 hypervisor?');
INSERT INTO Questions VALUES(43,'Which is the appropriate phase of the cloud data lifecycle for determining the data''s classification?');
INSERT INTO Questions VALUES(44,'Which of the following is the optimal temperature for a data center, per the guidelines established by the America Society of Heating, Refrigeration, and Air Conditioning Engineers (ASHRAE)?');
INSERT INTO Questions VALUES(45,'Which of the following is not a risk management framework?');
INSERT INTO Questions VALUES(46,'Which of the following threat types involves the sending of untrusted data to a user''s browser to be executed with their own credentials and access?');
INSERT INTO Questions VALUES(47,'How is an object stored within an object storage system?');
INSERT INTO Questions VALUES(48,'Which of the following is NOT a regulatory system from the United States federal government?');
INSERT INTO Questions VALUES(49,'Which jurisdiction lacks specific and comprehensive privacy laws at a national or top level of legal authority?');
INSERT INTO Questions VALUES(50,'Which United States law is focused on PII as it relates to the financial industry?');
INSERT INTO Questions VALUES(51,'Which of the following threat types can occur when encryption is not properly applied or insecure transport mechanisms are used?');
INSERT INTO Questions VALUES(52,'What is the best approach for dealing with services or utilities that are installed on a system but not needed to perform their desired function?');
INSERT INTO Questions VALUES(53,'Which of the following actions will NOT make data part of the create phase of the cloud data lifecycle?');
INSERT INTO Questions VALUES(54,'What are the two protocols that TLS uses?');
INSERT INTO Questions VALUES(55,'What are the two protocols that TLS uses?');
INSERT INTO Questions VALUES(56,'Which type of cloud model typically presents the most challenges to a cloud customer during the destroy phase of the cloud data lifecycle?');
INSERT INTO Questions VALUES(57,'Which of the following may unilaterally deem a cloud hosting model inappropriate for a system or application?');
INSERT INTO Questions VALUES(58,'Which of the following is considered an internal redundancy for a data center?');
INSERT INTO Questions VALUES(59,'Which of the following represents a control on the maximum amount of resources that a single customer, virtual machine, or application can consume within a cloud environment?');
INSERT INTO Questions VALUES(60,'Which of the following roles is responsible for peering with other cloud services and providers?');
INSERT INTO Questions VALUES(61,'Which of the following does NOT relate to the hiding of sensitive data from data sets?');
INSERT INTO Questions VALUES(62,'Which of the following are the storage types associated with IaaS?');
INSERT INTO Questions VALUES(63,'Which technology can be useful during the share phase of the cloud data lifecycle to continue to protect data as it leaves the original system and security controls?');
INSERT INTO Questions VALUES(64,'Which of the following storage types is most closely associated with a traditional file system and tree structure?');
INSERT INTO Questions VALUES(65,'Which of the following represents a prioritization of applications or cloud customers for the allocation of additional requested resources when there is a limitation on available resources?');
INSERT INTO Questions VALUES(66,'Which type of audit report does many cloud providers use to instill confidence in their policies, practices, and procedures to current and potential customers?');
INSERT INTO Questions VALUES(67,'Which of the following statements accurately describes VLANs?');
INSERT INTO Questions VALUES(68,'What must be secured on physical hardware to prevent unauthorized access to systems?');
INSERT INTO Questions VALUES(69,'What type of PII is regulated based on the type of application or per the conditions of the specific hosting agreement?');
INSERT INTO Questions VALUES(70,'Which of the following security technologies is commonly used to give administrators access into trust zones within an environment?');
INSERT INTO Questions VALUES(71,'Which concept BEST describes the capability for a cloud environment to automatically scale a system or application, based on its current resource demands?');
CREATE TABLE Answers (
    AnswerID INTEGER PRIMARY KEY,
    QuestionID INTEGER,
    AnswerText TEXT,
    IsCorrect BOOLEAN
);
INSERT INTO Answers VALUES(1,1,'Security policies',0);
INSERT INTO Answers VALUES(2,1,'Manual pages',0);
INSERT INTO Answers VALUES(3,1,'Vendor documentation',1);
INSERT INTO Answers VALUES(4,1,'Regulations',0);
INSERT INTO Answers VALUES(5,2,'Cloud auditor',0);
INSERT INTO Answers VALUES(6,2,'Inter-cloud provider',0);
INSERT INTO Answers VALUES(7,2,'Cloud service broker',0);
INSERT INTO Answers VALUES(8,2,'Cloud service developer',1);
INSERT INTO Answers VALUES(9,3,'Scope of processing',0);
INSERT INTO Answers VALUES(10,3,'Value of data',1);
INSERT INTO Answers VALUES(11,3,'Location of data',0);
INSERT INTO Answers VALUES(12,3,'Use of subcontractors',0);
INSERT INTO Answers VALUES(13,4,'Consumable service',0);
INSERT INTO Answers VALUES(14,4,'Measured service',1);
INSERT INTO Answers VALUES(15,4,'Billable service',0);
INSERT INTO Answers VALUES(16,4,'Metered service',0);
INSERT INTO Answers VALUES(17,5,'Cloud service integrator',0);
INSERT INTO Answers VALUES(18,5,'Cloud service business manager',0);
INSERT INTO Answers VALUES(19,5,'Cloud service user',0);
INSERT INTO Answers VALUES(20,5,'Cloud service administrator',1);
INSERT INTO Answers VALUES(21,6,'HTML',0);
INSERT INTO Answers VALUES(22,6,'SAML',0);
INSERT INTO Answers VALUES(23,6,'XSML',0);
INSERT INTO Answers VALUES(24,6,'XML',1);
INSERT INTO Answers VALUES(25,7,'JSON and SAML',0);
INSERT INTO Answers VALUES(26,7,'XML and SAML',0);
INSERT INTO Answers VALUES(27,7,'SAML and HTML',0);
INSERT INTO Answers VALUES(28,7,'XML and JSON',1);
INSERT INTO Answers VALUES(29,8,'Injection',0);
INSERT INTO Answers VALUES(30,8,'Cross-site scripting',0);
INSERT INTO Answers VALUES(31,8,'Cross-site request forgery',0);
INSERT INTO Answers VALUES(32,8,'Missing function-level access control',1);
INSERT INTO Answers VALUES(33,9,'Cloud service integrator',0);
INSERT INTO Answers VALUES(34,9,'Cloud service administrator',0);
INSERT INTO Answers VALUES(35,9,'Cloud service user',0);
INSERT INTO Answers VALUES(36,9,'Cloud service business manager',1);
INSERT INTO Answers VALUES(37,10,'Confidentiality',0);
INSERT INTO Answers VALUES(38,10,'Portability',0);
INSERT INTO Answers VALUES(39,10,'Availability',1);
INSERT INTO Answers VALUES(40,10,'Integrity',0);
INSERT INTO Answers VALUES(41,11,'Cryptographic erasure',0);
INSERT INTO Answers VALUES(42,11,'Zeroing',0);
INSERT INTO Answers VALUES(43,11,'Overwriting',0);
INSERT INTO Answers VALUES(44,11,'Deletion',1);
INSERT INTO Answers VALUES(45,12,'Resource pooling',0);
INSERT INTO Answers VALUES(46,12,'On-demand self-service',0);
INSERT INTO Answers VALUES(47,12,'Multitenancy',1);
INSERT INTO Answers VALUES(48,12,'Measured service',0);
INSERT INTO Answers VALUES(49,13,'Scripts',0);
INSERT INTO Answers VALUES(50,13,'RDP',0);
INSERT INTO Answers VALUES(51,13,'APIs',1);
INSERT INTO Answers VALUES(52,13,'XML',0);
INSERT INTO Answers VALUES(53,14,'Different certifications',0);
INSERT INTO Answers VALUES(54,14,'Multiple jurisdictions',1);
INSERT INTO Answers VALUES(55,14,'Different capabilities',0);
INSERT INTO Answers VALUES(56,14,'Different operational procedures',0);
INSERT INTO Answers VALUES(57,15,'LAN',0);
INSERT INTO Answers VALUES(58,15,'VLAN',1);
INSERT INTO Answers VALUES(59,15,'WAN',0);
INSERT INTO Answers VALUES(60,15,'PLAN',0);
INSERT INTO Answers VALUES(61,16,'IDCA',0);
INSERT INTO Answers VALUES(62,16,'BICSI',1);
INSERT INTO Answers VALUES(63,16,'NFPA',0);
INSERT INTO Answers VALUES(64,16,'Uptime Institute',0);
INSERT INTO Answers VALUES(65,17,'IDCA',0);
INSERT INTO Answers VALUES(66,17,'BICSI',0);
INSERT INTO Answers VALUES(67,17,'NFPA',0);
INSERT INTO Answers VALUES(68,17,'Uptime Institute',1);
INSERT INTO Answers VALUES(69,18,'Virtual',0);
INSERT INTO Answers VALUES(70,18,'Security',0);
INSERT INTO Answers VALUES(71,18,'Physical',0);
INSERT INTO Answers VALUES(72,18,'Logical',1);
INSERT INTO Answers VALUES(73,19,'Safe Harbor',0);
INSERT INTO Answers VALUES(74,19,'SOX',0);
INSERT INTO Answers VALUES(75,19,'GLBA',0);
INSERT INTO Answers VALUES(76,19,'HIPAA',1);
INSERT INTO Answers VALUES(77,20,'SSH',0);
INSERT INTO Answers VALUES(78,20,'VPN',0);
INSERT INTO Answers VALUES(79,20,'RDP',0);
INSERT INTO Answers VALUES(80,20,'KVM',1);
INSERT INTO Answers VALUES(81,21,'CPU',0);
INSERT INTO Answers VALUES(82,21,'Storage',0);
INSERT INTO Answers VALUES(83,21,'Memory',0);
INSERT INTO Answers VALUES(84,21,'Number of Users',1);
INSERT INTO Answers VALUES(85,22,'Possession',0);
INSERT INTO Answers VALUES(86,22,'Custody',0);
INSERT INTO Answers VALUES(87,22,'Control',0);
INSERT INTO Answers VALUES(88,22,'Archive',1);
INSERT INTO Answers VALUES(89,23,'HIPAA',0);
INSERT INTO Answers VALUES(90,23,'Safe Harbor',0);
INSERT INTO Answers VALUES(91,23,'GLBA',0);
INSERT INTO Answers VALUES(92,23,'SOX',1);
INSERT INTO Answers VALUES(93,24,'Dynamic',0);
INSERT INTO Answers VALUES(94,24,'Replication',0);
INSERT INTO Answers VALUES(95,24,'Duplication',0);
INSERT INTO Answers VALUES(96,24,'Static',1);
INSERT INTO Answers VALUES(97,25,'Object',0);
INSERT INTO Answers VALUES(98,25,'Unstructured',0);
INSERT INTO Answers VALUES(99,25,'Volume',0);
INSERT INTO Answers VALUES(100,25,'Structured',1);
INSERT INTO Answers VALUES(101,26,'Cloud service manager',0);
INSERT INTO Answers VALUES(102,26,'Cloud service deployment',0);
INSERT INTO Answers VALUES(103,26,'Cloud service operations manager',0);
INSERT INTO Answers VALUES(104,26,'Cloud service business manager',1);
INSERT INTO Answers VALUES(105,27,'SAML',0);
INSERT INTO Answers VALUES(106,27,'SSH',0);
INSERT INTO Answers VALUES(107,27,'XML',0);
INSERT INTO Answers VALUES(108,27,'HTTP',1);
INSERT INTO Answers VALUES(109,28,'SOX',0);
INSERT INTO Answers VALUES(110,28,'GLBA',0);
INSERT INTO Answers VALUES(111,28,'HIPAA',0);
INSERT INTO Answers VALUES(112,28,'Safe Harbor',1);
INSERT INTO Answers VALUES(113,29,'Certification',0);
INSERT INTO Answers VALUES(114,29,'Control',0);
INSERT INTO Answers VALUES(115,29,'Regulation',0);
INSERT INTO Answers VALUES(116,29,'Costs',1);
INSERT INTO Answers VALUES(117,30,'Dedicated switches',0);
INSERT INTO Answers VALUES(118,30,'Direct connections',0);
INSERT INTO Answers VALUES(119,30,'Redundant network circuits',0);
INSERT INTO Answers VALUES(120,30,'Trust zones',1);
INSERT INTO Answers VALUES(121,31,'Elasticity',0);
INSERT INTO Answers VALUES(122,31,'Reversibility',0);
INSERT INTO Answers VALUES(123,31,'Interoperability',0);
INSERT INTO Answers VALUES(124,31,'Portability',1);
INSERT INTO Answers VALUES(125,32,'REST and SAML',0);
INSERT INTO Answers VALUES(126,32,'REST and XML',0);
INSERT INTO Answers VALUES(127,32,'XML and SAML',0);
INSERT INTO Answers VALUES(128,32,'SOAP and REST',1);
INSERT INTO Answers VALUES(129,33,'ISO/IEC 31000',0);
INSERT INTO Answers VALUES(130,33,'ISO/IEC 19888',0);
INSERT INTO Answers VALUES(131,33,'ISO/IEC 27001',0);
INSERT INTO Answers VALUES(132,33,'ISO/IEC 27050',1);
INSERT INTO Answers VALUES(133,34,'Inter-cloud provider',0);
INSERT INTO Answers VALUES(134,34,'Cloud auditor',0);
INSERT INTO Answers VALUES(135,34,'Cloud service developer',0);
INSERT INTO Answers VALUES(136,34,'Cloud service broker',1);
INSERT INTO Answers VALUES(137,35,'Measured',0);
INSERT INTO Answers VALUES(138,35,'Theoretical',0);
INSERT INTO Answers VALUES(139,35,'Methodical',0);
INSERT INTO Answers VALUES(140,35,'Forensics',1);
INSERT INTO Answers VALUES(141,36,'Cloud service deployment manager',0);
INSERT INTO Answers VALUES(142,36,'Cloud service business manager',0);
INSERT INTO Answers VALUES(143,36,'Cloud service operations manager',0);
INSERT INTO Answers VALUES(144,36,'Cloud service manager',1);
INSERT INTO Answers VALUES(145,37,'Different technology standards',0);
INSERT INTO Answers VALUES(146,37,'Costs',0);
INSERT INTO Answers VALUES(147,37,'Language barriers',0);
INSERT INTO Answers VALUES(148,37,'Lack of international authority',1);
INSERT INTO Answers VALUES(149,38,'ISO/IEC',0);
INSERT INTO Answers VALUES(150,38,'ISO',0);
INSERT INTO Answers VALUES(151,38,'PCI Council',0);
INSERT INTO Answers VALUES(152,38,'AICPA',1);
INSERT INTO Answers VALUES(153,39,'Cloud service business manager',0);
INSERT INTO Answers VALUES(154,39,'Cloud service deployment manager',0);
INSERT INTO Answers VALUES(155,39,'Cloud service manager',0);
INSERT INTO Answers VALUES(156,39,'Cloud service operations manager',1);
INSERT INTO Answers VALUES(157,40,'SCSI',0);
INSERT INTO Answers VALUES(158,40,'TLS',0);
INSERT INTO Answers VALUES(159,40,'SATA',0);
INSERT INTO Answers VALUES(160,40,'iSCSI',1);
INSERT INTO Answers VALUES(161,41,'Hybrid',0);
INSERT INTO Answers VALUES(162,41,'Community',0);
INSERT INTO Answers VALUES(163,41,'Private',0);
INSERT INTO Answers VALUES(164,41,'Public',1);
INSERT INTO Answers VALUES(165,42,'A Type 2 hypervisor is always exposed to the public Internet for federated identity access.',0);
INSERT INTO Answers VALUES(166,42,'A Type 2 hypervisor is open source, so attackers can more easily find exploitable vulnerabilities with that access.',0);
INSERT INTO Answers VALUES(167,42,'A Type 2 hypervisor allows users to directly perform some functions with their own access.',0);
INSERT INTO Answers VALUES(168,42,'A Type 2 hypervisor runs on top of another operating system and is dependent on the security of the OS for its own security.',1);
INSERT INTO Answers VALUES(169,43,'Store',0);
INSERT INTO Answers VALUES(170,43,'Share',0);
INSERT INTO Answers VALUES(171,43,'Use',0);
INSERT INTO Answers VALUES(172,43,'Create',1);
INSERT INTO Answers VALUES(173,44,'69.8-86.0degF (21-30degC)',0);
INSERT INTO Answers VALUES(174,44,'44.6-60-8degF(7-16degC)',0);
INSERT INTO Answers VALUES(175,44,'51.8-66.2degF(11-19degC)',0);
INSERT INTO Answers VALUES(176,44,'64.4-80.6degF(18-27degC)',1);
INSERT INTO Answers VALUES(177,45,'COBIT',0);
INSERT INTO Answers VALUES(178,45,'NIST SP 800-37',0);
INSERT INTO Answers VALUES(179,45,'ISO 31000:2009',0);
INSERT INTO Answers VALUES(180,45,'Hex GBL',1);
INSERT INTO Answers VALUES(181,46,'Missing function level access control',0);
INSERT INTO Answers VALUES(182,46,'Injection',0);
INSERT INTO Answers VALUES(183,46,'Cross-site request forgery',1);
INSERT INTO Answers VALUES(184,46,'Cross-site scripting',0);
INSERT INTO Answers VALUES(185,47,'Tree structure',0);
INSERT INTO Answers VALUES(186,47,'LDAP',0);
INSERT INTO Answers VALUES(187,47,'Key value',1);
INSERT INTO Answers VALUES(188,47,'Database',0);
INSERT INTO Answers VALUES(189,48,'HIPAA',0);
INSERT INTO Answers VALUES(190,48,'SOX',0);
INSERT INTO Answers VALUES(191,48,'PCI DSS',1);
INSERT INTO Answers VALUES(192,48,'FISMA',0);
INSERT INTO Answers VALUES(193,49,'European Union',0);
INSERT INTO Answers VALUES(194,49,'Germany',0);
INSERT INTO Answers VALUES(195,49,'United States',1);
INSERT INTO Answers VALUES(196,49,'Russia',0);
INSERT INTO Answers VALUES(197,50,'HIPAA',0);
INSERT INTO Answers VALUES(198,50,'SOX',0);
INSERT INTO Answers VALUES(199,50,'GLBA',1);
INSERT INTO Answers VALUES(200,50,'Safe Harbor',0);
INSERT INTO Answers VALUES(201,51,'Security misconfiguration',0);
INSERT INTO Answers VALUES(202,51,'Insecure direct object references',0);
INSERT INTO Answers VALUES(203,51,'Sensitive data exposure',1);
INSERT INTO Answers VALUES(204,51,'Unvalidated redirects and forwards',0);
INSERT INTO Answers VALUES(205,52,'Stop',0);
INSERT INTO Answers VALUES(206,52,'Disable',0);
INSERT INTO Answers VALUES(207,52,'Remove',1);
INSERT INTO Answers VALUES(208,52,'Monitor',0);
INSERT INTO Answers VALUES(209,53,'Constructing new data',0);
INSERT INTO Answers VALUES(210,53,'Modifying data',0);
INSERT INTO Answers VALUES(211,53,'Modifying metadata',1);
INSERT INTO Answers VALUES(212,53,'Importing data',0);
INSERT INTO Answers VALUES(213,54,'Handshake and record',1);
INSERT INTO Answers VALUES(214,54,'Transport and initiate',0);
INSERT INTO Answers VALUES(215,54,'Handshake and transport',0);
INSERT INTO Answers VALUES(216,54,'Record and transmit',0);
INSERT INTO Answers VALUES(217,55,'Handshake and record',1);
INSERT INTO Answers VALUES(218,55,'Transport and initiate',0);
INSERT INTO Answers VALUES(219,55,'Handshake and transport',0);
INSERT INTO Answers VALUES(220,55,'Record and transmit',0);
INSERT INTO Answers VALUES(221,56,'SaaS',1);
INSERT INTO Answers VALUES(222,56,'IaaS',0);
INSERT INTO Answers VALUES(223,56,'DaaS',0);
INSERT INTO Answers VALUES(224,56,'PaaS',0);
INSERT INTO Answers VALUES(225,57,'Regulation',1);
INSERT INTO Answers VALUES(226,57,'Multitenancy',0);
INSERT INTO Answers VALUES(227,57,'Certification',0);
INSERT INTO Answers VALUES(228,57,'Virtualization',0);
INSERT INTO Answers VALUES(229,58,'Power distribution units',1);
INSERT INTO Answers VALUES(230,58,'Network circuits',0);
INSERT INTO Answers VALUES(231,58,'Power substations',0);
INSERT INTO Answers VALUES(232,58,'Generators',0);
INSERT INTO Answers VALUES(233,59,'Share',0);
INSERT INTO Answers VALUES(234,59,'Reservation',0);
INSERT INTO Answers VALUES(235,59,'Provision',0);
INSERT INTO Answers VALUES(236,59,'Limit',1);
INSERT INTO Answers VALUES(237,60,'Cloud auditor',0);
INSERT INTO Answers VALUES(238,60,'Cloud service broker',0);
INSERT INTO Answers VALUES(239,60,'Cloud service developer',0);
INSERT INTO Answers VALUES(240,60,'Inter-cloud provider',1);
INSERT INTO Answers VALUES(241,61,'Obfuscation',0);
INSERT INTO Answers VALUES(242,61,'Masking',0);
INSERT INTO Answers VALUES(243,61,'Anonymization',0);
INSERT INTO Answers VALUES(244,61,'Federation',1);
INSERT INTO Answers VALUES(245,62,'Object and target',0);
INSERT INTO Answers VALUES(246,62,'Volume and container',0);
INSERT INTO Answers VALUES(247,62,'Volume and label',0);
INSERT INTO Answers VALUES(248,62,'Volume and object',1);
INSERT INTO Answers VALUES(249,63,'IPS',0);
INSERT INTO Answers VALUES(250,63,'WAF',0);
INSERT INTO Answers VALUES(251,63,'IDS',0);
INSERT INTO Answers VALUES(252,63,'DLP',1);
INSERT INTO Answers VALUES(253,64,'Structured',0);
INSERT INTO Answers VALUES(254,64,'Object',0);
INSERT INTO Answers VALUES(255,64,'Unstructured',0);
INSERT INTO Answers VALUES(256,64,'Volume',1);
INSERT INTO Answers VALUES(257,65,'Provision',0);
INSERT INTO Answers VALUES(258,65,'Limit',0);
INSERT INTO Answers VALUES(259,65,'Reservation',0);
INSERT INTO Answers VALUES(260,65,'Share',1);
INSERT INTO Answers VALUES(261,66,'SOX',0);
INSERT INTO Answers VALUES(262,66,'SOC 1',0);
INSERT INTO Answers VALUES(263,66,'SAS-70',0);
INSERT INTO Answers VALUES(264,66,'SOC 2',1);
INSERT INTO Answers VALUES(265,67,'They are not restricted to the same rack but restricted to same switches.',0);
INSERT INTO Answers VALUES(266,67,'They are restricted to the same racks and data centers.',0);
INSERT INTO Answers VALUES(267,67,'They are not restricted to the name rack but restricted to the same data center.',0);
INSERT INTO Answers VALUES(268,67,'They are not restricted to the same data center or the same racks.',1);
INSERT INTO Answers VALUES(269,68,'ALOM',0);
INSERT INTO Answers VALUES(270,68,'RDP',0);
INSERT INTO Answers VALUES(271,68,'SSH',0);
INSERT INTO Answers VALUES(272,68,'BIOS',1);
INSERT INTO Answers VALUES(273,69,'Specific',0);
INSERT INTO Answers VALUES(274,69,'Regulated',0);
INSERT INTO Answers VALUES(275,69,'Jurisdictional',0);
INSERT INTO Answers VALUES(276,69,'Contractual',1);
INSERT INTO Answers VALUES(277,70,'HTTPS',0);
INSERT INTO Answers VALUES(278,70,'IPSec',0);
INSERT INTO Answers VALUES(279,70,'WAF',0);
INSERT INTO Answers VALUES(280,70,'VPN',1);
INSERT INTO Answers VALUES(281,71,'On-demand self-service',0);
INSERT INTO Answers VALUES(282,71,'Resource pooling',0);
INSERT INTO Answers VALUES(283,71,'Measured service',0);
INSERT INTO Answers VALUES(284,71,'Rapid elasticity',1);
COMMIT;
