

# What is this?
This is a python script to generate golang struct from mysql.
## Example:
```SQL
CREATE TABLE CUSTOMER (
  `ID`                    INT           NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `COMPANY_ID`            INT           NOT NULL,
  `NAME`                  VARCHAR(50)   NOT NULL,
  `SHORT_NAME`            VARCHAR(20)   NULL,
  `DELIVERY_ADDRESS`      VARCHAR(300)  NULL,
  `INDUSTRY_CATEGORY_ID`  INT           NULL,
  `INDUSTRY_ID`           INT           NULL,
  `CAPITAL`               DECIMAL(16)   NULL
  `RATING`                INT           NULL
  `ANNUAL_REVENUE`        DECIMAL(16)   NULL
  `PROVINCE_ID`           INT           NULL
  `ADDRESS_1`             VARCHAR(50)   NULL
  `ADDRESS_2`             VARCHAR(50)   NULL
  `ADDRESS_3`             VARCHAR(50)   NULL
  `ZIP_CODE`              VARCHAR(10)   NULL,
  `TEL`                   VARCHAR(16)   NULL,
  `FAX`                   VARCHAR(16)   NULL,
  `IS_OVERSEA_COMPANY`    BOOLEAN       NOT NULL DEFAULT false,
  `SITE_URL`              VARCHAR(511)  NULL,
  `REGISTER_ID`           INT           NOT NULL
  `DELETED`               BOOLEAN       NOT NULL DEFAULT FALSE,
  `CREATED_AT`            TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `UPDATED_AT`            TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
   INDEX                  COMPANY_ID_INDEX(COMPANY_ID),
   INDEX                  CREATED_AT_INDEX(CREATED_AT),
   INDEX                  UPDATED_AT_INDEX(UPDATED_AT)
) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;
```

## Generated go code
```go
package entities

import (
	"time"

	"github.com/guregu/null"
)

// Customer Entity
type Customer struct {
	ID                 int         `xorm:"'ID' pk autoincr"`
	CompanyID          int         `xorm:"'COMPANY_ID'"`
	Name               string      `xorm:"'NAME'"`
	ShortName          null.String `xorm:"'SHORT_NAME'"`
	DeliveryAddress    null.String `xorm:"'DELIVERY_ADDRESS'"`
	IndustryCategoryID null.Int    `xorm:"'INDUSTRY_CATEGORY_ID'"`
	IndustryID         null.Int    `xorm:"'INDUSTRY_ID'"`
	Capital            null.Float  `xorm:"'CAPITAL'"`
	Rating             null.Int    `xorm:"'RATING'"`
	AnnualRevenue      null.Float  `xorm:"'ANNUAL_REVENUE'"`
	ProvinceID         int         `xorm:"'PROVINCE_ID'"`
	Address1           null.String `xorm:"'ADDRESS_1'"`
	Address2           null.String `xorm:"'ADDRESS_2'"`
	Address3           null.String `xorm:"'ADDRESS_3'"`
	ZipCode            null.String `xorm:"'ZIP_CODE'"`
	Tel                null.String `xorm:"'TEL'"`
	Fax                null.String `xorm:"'FAX'"`
	IsOverseaCompany   bool        `xorm:"'IS_OVERSEA_COMPANY'"`
	WebSiteURL         null.String `xorm:"'WEB_SITE_URL'"`
	RegisterID         int         `xorm:"'REGISTER_ID'"`
	Deleted            bool        `xorm:"'DELETED'"`
	CreatedAt          time.Time   `xorm:"'CREATED_AT'"`
	UpdatedAt          time.Time   `xorm:"'UPDATED_AT'"`
}
```

# How to use
```bash
python generate.py --user=db_user --passwd=db_password --database=db_name --table_name=CUSTOMER > ./customer.go


options:
    -h, --help            show this help message and exit
    -u USER, --user USER  User for login if not current user
    -p PASSWD, --passwd PASSWD
                          Password to use when connecting to server.
    -P PORT, --port PORT  Port to use when connecting to server.
    -H HOST, --host HOST  Server host
    -d DATABASE, --database DATABASE
                          Database to use
    --package_name PACKAGE_NAME
                          Go package name
    -t TABLE_NAME, --table_name TABLE_NAME
                          Table name
    --charset CHARSET     Charset,default [utf8]
```

# Demo
![demo](https://user-images.githubusercontent.com/11124312/66663887-7c7f4880-ec86-11e9-8399-3b4803b14dd8.gif)
