CREATE TABLE CarBrand (
    BrandID INT PRIMARY KEY IDENTITY(1,1),
    BrandName NVARCHAR(50) NOT NULL UNIQUE,
    Country NVARCHAR(50)
)

CREATE TABLE CarModel (
    ModelID INT PRIMARY KEY IDENTITY(1,1),
    ModelName NVARCHAR(50) NOT NULL,
    BrandID INT NOT NULL,
    ProductionYear INT NOT NULL CHECK (ProductionYear >= 1300),
    FOREIGN KEY (BrandID) REFERENCES CarBrand(BrandID)
)

CREATE TABLE Customer (
    CustomerID INT PRIMARY KEY IDENTITY(1,1),
    FullName NVARCHAR(50) NOT NULL,
    NationalCode CHAR(10) NOT NULL UNIQUE,
    Mobile CHAR(11) NOT NULL,
    Phone CHAR(11),
    Address NVARCHAR(200) NOT NULL,
    PostalCode CHAR(10)
)

CREATE TABLE Staff (
    StaffID INT PRIMARY KEY IDENTITY(1,1),
    FullName NVARCHAR(100) NOT NULL,
    Role NVARCHAR(100) NOT NULL,
    NationalCode CHAR(10) NOT NULL UNIQUE
)

CREATE TABLE Car (
    CarID INT PRIMARY KEY IDENTITY(1,1),
    LicensePlate NVARCHAR(15) NOT NULL UNIQUE,
    ChassisNumber NVARCHAR(20) NOT NULL UNIQUE,
    EngineNumber NVARCHAR(50) NOT NULL UNIQUE,
    Color NVARCHAR(30) NOT NULL,
    GearboxType NVARCHAR(30) NOT NULL,
    BodyType NVARCHAR(30) NOT NULL,
    EngineType NVARCHAR(30) NOT NULL,
    ModelID INT NOT NULL,
    CustomerID INT NOT NULL,
    FOREIGN KEY (ModelID) REFERENCES CarModel(ModelID),
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
)

CREATE TABLE Reception (
    ReceptionID INT PRIMARY KEY IDENTITY(1,1),
    ReceptionDate DATE NOT NULL,
    Status NVARCHAR(30),
    KilometerIn INT,
    KilometerOut INT,
    EstimatedCost INT,
    CarID INT NOT NULL,
    FOREIGN KEY (CarID) REFERENCES Car(CarID)
)

CREATE TABLE RepairOrder (
    RepairOrderID INT PRIMARY KEY IDENTITY(1,1),
    OrderDate DATE,
    Status NVARCHAR(30),
    Description NVARCHAR(255),
    ReceptionID INT NOT NULL,
    FOREIGN KEY (ReceptionID) REFERENCES Reception(ReceptionID)
)

CREATE TABLE Goods (
    GoodsID INT PRIMARY KEY IDENTITY(1,1),
    GoodsName NVARCHAR(100),
    Brand NVARCHAR(50),
    UnitPrice INT
)

CREATE TABLE Service (
    ServiceID INT PRIMARY KEY IDENTITY(1,1),
    ServiceName NVARCHAR(100),
    Description NVARCHAR(255),
    Cost INT
)

CREATE TABLE Part_Used (
    UsedPartID INT PRIMARY KEY IDENTITY(1,1),
    QuantityUsed INT,
    RepairOrderID INT NOT NULL,
    GoodsID INT NOT NULL,
    FOREIGN KEY (RepairOrderID) REFERENCES RepairOrder(RepairOrderID),
    FOREIGN KEY (GoodsID) REFERENCES Goods(GoodsID)
)

CREATE TABLE RepairOrderService (
    RepairOrderID INT NOT NULL,
    ServiceID INT NOT NULL,
    PRIMARY KEY (RepairOrderID, ServiceID),
    FOREIGN KEY (RepairOrderID) REFERENCES RepairOrder(RepairOrderID),
    FOREIGN KEY (ServiceID) REFERENCES Service(ServiceID)
)

CREATE TABLE RepairOrderStaff (
    RepairOrderID INT NOT NULL,
    StaffID INT NOT NULL,
    RoleInRepair NVARCHAR(50),
    PRIMARY KEY (RepairOrderID, StaffID),
    FOREIGN KEY (RepairOrderID) REFERENCES RepairOrder(RepairOrderID),
    FOREIGN KEY (StaffID) REFERENCES Staff(StaffID)
)