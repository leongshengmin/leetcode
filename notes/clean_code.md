# Software Engineering Principles
## 1. Dependency Inversion (DIP)
> High-level modules should not depend on low-level modules. Both should depend on abstractions. Abstractions should not depend on details. Details should depend on abstractions.
i.e application level code eg. http handler should rely on interfaces (DAO) to access the data layer. This allows the data layer interface to be replaced with a mock class implementing the interface.

**DIP Violation**
The Infrastructure Layer
```
type UserRepository struct {
	db *gorm.DB
}

func NewUserRepository(db *gorm.DB) *UserRepository {
	return &UserRepository{
		db: db,
	}
}

func (r *UserRepository) GetByID(id uint) (*domain.User, error) {
	user := domain.User{}
	err := r.db.Where("id = ?", id).First(&user).Error
	if err != nil {
		return nil, err
	}

	return &user, nil
}
```
The Domain Layer
```
type User struct {
	ID uint `gorm:"primaryKey;column:id"`
	// some fields
}

The Application Layer

type EmailService struct {
	repository *infrastructure.UserRepository
	// some email sender
}

func NewEmailService(repository *infrastructure.UserRepository) *EmailService {
	return &EmailService{
		repository: repository,
	}
}

func (s *EmailService) SendRegistrationEmail(userID uint) error {
	user, err := s.repository.GetByID(userID)
	if err != nil {
		return err
	}
	// send email
	return nil
}
```
In the code snippet above, we defined a high-level component, EmailService (Application Layer) which contains a UserRepository struct (rather than an interface of UserRepository) that operates at Infrastructure Layer. Since we're storing the actual struct rather than interface, during testing we have to initialize the UserRepository object and the database connection to create the EmailService object and so we are NOT relying on abstractions.

**Corrected version**
Note:
- separate struct used for `UserGorm` (data layer) and `User` (domain layer).
- infra layer `UserDatabaseRepository` struct now implicitly implements `UserRepository` interface && application layer communicates with data layer via this interface (`EmailService` struct contains `UserRepository` interface now instead of the data layer struct).

Infra layer
```
type UserGorm struct {
	// some fields
}

func (g UserGorm) ToUser() *domain.User {
	return &domain.User{
		// some fields
	}
}

type UserDatabaseRepository struct {
	db *gorm.DB
}

var _ domain.UserRepository = &UserDatabaseRepository{}

func NewUserDatabaseRepository(db *gorm.DB) UserRepository {
	return &UserDatabaseRepository{
		db: db,
	}
}

func (r *UserDatabaseRepository) GetByID(id uint) (*domain.User, error) {
	user := UserGorm{}
	err := r.db.Where("id = ?", id).First(&user).Error
	if err != nil {
		return nil, err
	}

	return user.ToUser(), nil
}
```
Domain layer
```
type User struct {
	// some fields
}

type UserRepository interface {
	GetByID(id uint) (*User, error)
}
```
The Application Layer
```
type EmailService struct {
	repository domain.UserRepository
	// some email sender
}

func NewEmailService(repository domain.UserRepository) *EmailService {
	return &EmailService{
		repository: repository,
	}
}

func (s *EmailService) SendRegistrationEmail(userID uint) error {
	user, err := s.repository.GetByID(userID)
	if err != nil {
		return err
	}
	// send email
	return nil
}
```

## 2. Single Responsibility Principle (SRP)
>The Single Responsibility Principle (SRP) asserts that each software module should serve a single, specific purpose that could lead to change.

**Eg.1 SRP violation by function doing way too many things**
The responsibility of the EmailService is not limited to sending emails; it also involves storing an email message in the database and sending it via the SMTP protocol.
```
...
func (s *EmailService) Send(from string, to string, subject string, message string) error {
	email := EmailGorm{
		From:    from,
		To:      to,
		Subject: subject,
		Message: message,
	}

	err := s.db.Create(&email).Error
	if err != nil {
		log.Println(err)
		return err
	}
	
	auth := smtp.PlainAuth("", from, s.smtpPassword, s.smtpHost)
	
	server := fmt.Sprintf("%s:%d", s.smtpHost, s.smtpPort)
	
	err = smtp.SendMail(server, auth, from, []string{to}, []byte(message))
	if err != nil {
		log.Println(err)
		return err
	}

	return nil
}
```

**Fixed code**
EmailRepository
```
type EmailGorm struct {
	gorm.Model
	From    string
	To      string
	Subject string
	Message string
}

type EmailRepository interface {
	Save(from string, to string, subject string, message string) error
}

type EmailDBRepository struct {
	db *gorm.DB
}

func NewEmailRepository(db *gorm.DB) EmailRepository {
	return &EmailDBRepository{
		db: db,
	}
}

func (r *EmailDBRepository) Save(from string, to string, subject string, message string) error {
	email := EmailGorm{
		From:    from,
		To:      to,
		Subject: subject,
		Message: message,
	}

	err := r.db.Create(&email).Error
	if err != nil {
		log.Println(err)
		return err
	}

	return nil
}
```
EmailSender
```
type EmailSender interface {
	Send(from string, to string, subject string, message string) error
}

type EmailSMTPSender struct {
	smtpHost     string
	smtpPassword string
	smtpPort     int
}

func NewEmailSender(smtpHost string, smtpPassword string, smtpPort int) EmailSender {
	return &EmailSMTPSender{
		smtpHost:     smtpHost,
		smtpPassword: smtpPassword,
		smtpPort:     smtpPort,
	}
}

func (s *EmailSMTPSender) Send(from string, to string, subject string, message string) error {
	auth := smtp.PlainAuth("", from, s.smtpPassword, s.smtpHost)

	server := fmt.Sprintf("%s:%d", s.smtpHost, s.smtpPort)

	err := smtp.SendMail(server, auth, from, []string{to}, []byte(message))
	if err != nil {
		log.Println(err)
		return err
	}

	return nil
}
```
EmailService
```
type EmailService struct {
	repository EmailRepository
	sender     EmailSender
}

func NewEmailService(repository EmailRepository, sender EmailSender) *EmailService {
	return &EmailService{
		repository: repository,
		sender:     sender,
	}
}

func (s *EmailService) Send(from string, to string, subject string, message string) error {
	err := s.repository.Save(from, to, subject, message)
	if err != nil {
		return err
	}

	return s.sender.Send(from, to, subject, message)
}
```

**Eg2.1 SRP violated by struct doing too many things**
```
type User struct {
	db *gorm.DB // handles db conn
	Username string // yet also contains entity details
	Firstname string
	Lastname string
	Birthday time.Time
	//
	// some more fields
	//
}

func (u User) IsAdult() bool {
	return u.Birthday.AddDate(18, 0, 0).Before(time.Now())
}

func (u *User) Save() error {
	return u.db.Exec("INSERT INTO users ...", u.Username, u.Firstname, u.Lastname, u.Birthday).Error
}
```
**Eg2.2 SRP violated by struct doing too many things**
```
type Transaction struct {
	gorm.Model
	Amount     int       `gorm:"column:amount" json:"amount" validate:"required"` // same entity used to serve as a mapping to a database table, act as a holder for JSON responses in a REST API
	CurrencyID int       `gorm:"column:currency_id" json:"currency_id" validate:"required"`
	Time       time.Time `gorm:"column:time" json:"time" validate:"required"`
}
```

## 3. Interface Segregation Principle (ISP)
>Maintain small interfaces to prevent users from relying on unnecessary features.

This helps to reduce the bloat in interfaces, preventing the need to just mock a subset of functions in interface. Ideally we should use smaller custom interfaces as 3rd party libs may contain many methods in the interface that we don't use yet have to implement if we want to unit test.

**Mocking Subset of Functions in Interface**
Sometimes, there is no need to mock all the methods from the interface, or the package is not under our control, preventing us from generating files. It also doesn’t make sense to create and maintain files in our library. However, there are instances when an interface contains numerous methods, and we only need a subset of them. In such cases, we can use an example with UserRepository. AdminController utilizes only one function from the Repository, which is FilterByLastname. This means we don’t require any other methods to test AdminController. To address this, let’s create a struct called MockedUserRepository, as shown in the example below:
```
MockedUserRepository struct

type MockedUserRepository struct {
	UserRepository // MockedUserRepository struct contains an interface -- this implicitly means that MockedUserRepository struct implements all methods in UserRepository
	filterByLastnameFunc func(ctx context.Context, lastname string) ([]User, error)
}
// for overriding the FilterByLastname method in UserRepository interface
// other non-overriden methods will be 'proxied' to the actual UserRepository
func (r *MockedUserRepository) FilterByLastname(ctx context.Context, lastname string) ([]User, error) {
	return r.filterByLastnameFunc(ctx, lastname)
}
```
MockedUserRepository implements the UserRepository interface. We ensured this by embedding the UserRepository interface inside MockedUserRepository. Our mock object expects to contain an instance of the UserRepository interface within it. If that instance is not defined, it will default to nil. Additionally, it has one field, which is a function type with the same signature as FilterByLastname. The FilterByLastname method is attached to the mocked struct, and it simply forwards calls to this private field. Now, if we rewrite our test as follows, it may appear more intuitive:

File /pkg/user/admin_controller_test.go
```
func TestAdminController(t *testing.T) {
	var gCtx *gin.Context
	//
	// setup context
	//

	repository := &MockedUserRepository{}
	repository.filterByLastnameFunc = func(ctx context.Context, lastname string) ([]User, error) {
		if ctx != gCtx {
			t.Error("expected other context")
		}
		
		if lastname != "some last name" {
			t.Error("expected other lastname")
		}
		return nil, errors.New("error")
	}

	controller := NewAdminController(repository)
	controller.FilterByLastname(gCtx)
	//
	// do some checking for ctx
	//
}
```
This technique can be beneficial when testing our code’s integration with AWS services, such as SQS, using the AWS SDK. In this case, our SQSReceiver depends on the SQSAPI interface, which has many functions:

SQSReceiver
```
import (
	//
	// some imports
	//
	"github.com/aws/aws-sdk-go/service/sqs/sqsiface"
)

type SQSReceiver struct {
	sqsAPI sqsiface.SQSAPI
}

func (r *SQSReceiver) Run() {
	//
	// wait for SQS message
	//
}
```
Here we can use the same technique and provide our own mocked struct:

MockedSQSAPI
```
type MockedSQSAPI struct {
	sqsiface.SQSAPI
	sendMessageFunc func(input *sqs.SendMessageInput) (*sqs.SendMessageOutput, error)
}

func (m *MockedSQSAPI) SendMessage(input *sqs.SendMessageInput) (*sqs.SendMessageOutput, error) {
	return m.sendMessageFunc(input)
}
```
Test SQSReceiver
```
func TestSQSReceiver(t *testing.T) {
	//
	// setup context
	//

	sqsAPI := &MockedSQSAPI{}
	sqsAPI.sendMessageFunc = func(input *sqs.SendMessageInput) (*sqs.SendMessageOutput, error) {
		if input.MessageBody == nil || *input.MessageBody != "content" {
			t.Error("expected other message")
		}

		return nil, errors.New("error")
	}

	receiver := &SQSReceiver{
		sqsAPI: sqsAPI,
	}

	receiver.Run()
	//
	// do some checking for ctx
	//
}
```

**ISP violation**
We have implemented this interface with three structs. The first one is the Guest struct, representing a user who is not logged in but can still add a Product to the ShoppingCart. The second implementation is the NormalCustomer, which can do everything a Guest can, plus make a purchase. The third implementation is the PremiumCustomer, which can use all features of our system.

NormalCustomer struct
```
type NormalCustomer struct {
	cart   ShoppingCart
	wallet Wallet
	//
	// some additional fields
	//
}

func (c *NormalCustomer) AddToShoppingCart(product Product) {
	c.cart.Add(product)
}

func (c *NormalCustomer) IsLoggedIn() bool {
	return true
}

func (c *NormalCustomer) Pay(money Money) error {
	return c.wallet.Deduct(money)
}

func (c *NormalCustomer) HasPremium() bool {
	return false
}

func (c *NormalCustomer) HasDiscountFor(Product) bool {
	return false
}
```
PremiumCustomer struct
```
type PremiumCustomer struct {
	cart     ShoppingCart
	wallet   Wallet
	policies []DiscountPolicy
	//
	// some additional fields
	//
}

func (c *PremiumCustomer) AddToShoppingCart(product Product) {
	c.cart.Add(product)
}

func (c *PremiumCustomer) IsLoggedIn() bool {
	return true
}

func (c *PremiumCustomer) Pay(money Money) error {
	return c.wallet.Deduct(money)
}

func (c *PremiumCustomer) HasPremium() bool {
	return true
}

func (c *PremiumCustomer) HasDiscountFor(product Product) bool {
	for _, p := range c.policies {
		if p.IsApplicableFor(c, product) {
			return true
		}
	}
	
	return false
}
```
Now, take a closer look at all three structs. Only the PremiumCustomer requires all three methods. Perhaps we could assign all of them to the NormalCustomer, but definitely, we hardly need more than two methods for the Guest. Methods like HasPremium and HasDiscountFor don’t make sense for a Guest. If this struct represents a User who is not logged in, why would we even consider implementing methods for discounts? In such cases, we might even call the panic method with the error message “method is not implemented” — that would be more honest in this code. In a typical scenario, we shouldn’t even call the HasPremium method from a Guest.

**Fixed code**
```
type User interface {
	AddToShoppingCart(product Product)
	//
	// some additional methods
	//
}

type LoggedInUser interface {
	User
	Pay(money Money) error
	//
	// some additional methods
	//
}

type PremiumUser interface {
	LoggedInUser
	HasDiscountFor(product Product) bool
	//
	// some additional methods
	//
}
```
Now, instead of one interface, we have three: PremiumUser embeds LoggedInUser, which embeds User. Additionally, each of them introduces one method. The User interface now represents only customers who are still not authenticated on our platform. For such types, we know they can use features of the ShoppingCart. The new LoggedInUser interface represents all our authenticated customers, and the PremiumUser interface represents all authenticated customers with a paid premium account.

Concrete User implementations
```
type Guest struct {
	cart ShoppingCart
	//
	// some additional fields
	//
}

// Guest struct just implements 1 method -- AddToShoppingCart
func (g *Guest) AddToShoppingCart(product Product) {
	g.cart.Add(product)
}

type NormalCustomer struct {
	cart   ShoppingCart
	wallet Wallet
	//
	// some additional fields
	//
}

// NormalCustomer struct implements 2 -- AddToShoppingCart, Pay
func (c *NormalCustomer) AddToShoppingCart(product Product) {
	c.cart.Add(product)
}

func (c *NormalCustomer) Pay(money Money) error {
	return c.wallet.Deduct(money)
}

type PremiumCustomer struct {
	cart     ShoppingCart
	wallet   Wallet
	policies []DiscountPolicy
	//
	// some additional fields
	//
}

func (c *PremiumCustomer) AddToShoppingCart(product Product) {
	c.cart.Add(product)
}

func (c *PremiumCustomer) Pay(money Money) error {
	return c.wallet.Deduct(money)
}

func (c *PremiumCustomer) HasDiscountFor(product Product) bool {
	for _, p := range c.policies {
		if p.IsApplicableFor(c, product) {
			return true
		}
	}

	return false
}
```

## 4. Liskov Substitution Principle (LSP)
**Violation**
```
type ConvexQuadrilateral interface {
	GetArea() int
}

type Rectangle interface {
	ConvexQuadrilateral
	SetA(a int)
	SetB(b int)
}

type Oblong struct {
	Rectangle
	a int
	b int
}

func (o *Oblong) SetA(a int) {
	o.a = a
}

func (o *Oblong) SetB(b int) {
	o.b = b
}

func (o Oblong) GetArea() int {
	return o.a * o.b
}

type Square struct {
	Rectangle
	a int
}

func (o *Square) SetA(a int) {
	o.a = a
}

func (o Square) GetArea() int {
	return o.a * o.a
}

func (o *Square) SetB(b int) {
	//
	// should it be o.a = b ?
	// or should it be empty?
	//
}
```
Next, we have the actual implementations. The first one is Oblong, which can have either a wider width or a wider height. In geometry, it refers to any rectangle that is not a square. Implementing the logic for this struct is straightforward.

The second subtype of Rectangle is Square. In geometry, a square is considered a subtype of a rectangle. However, if we follow this subtyping relationship in software development, we encounter an issue. A square has all four sides equal, making the SetB method obsolete. To adhere to the initial subtyping structure we chose, we end up with obsolete methods in our code.

**Fixed code**
```
type EquilateralQuadrilateral interface {
	ConvexQuadrilateral
	SetA(a int)
}

type NonEquilateralQuadrilateral interface {
	ConvexQuadrilateral
	SetA(a int)
	SetB(b int)
}

type Oblong struct {
	NonEquilateralQuadrilateral
	a int
	b int
}

type Square struct {
	EquilateralQuadrilateral
	a int
}
```
To support subtyping for geometrical shapes in Go, it’s crucial to consider all of their features to avoid broken or obsolete methods. In this case, we introduced 2 new interfaces: EquilateralQuadrilateral (representing a quadrilateral with all four equal sides), NonEquilateralQuadrilateral (representing a quadrilateral with two pairs of equal sides). Each of these interfaces provides additional methods necessary to supply the required data for area calculation and setting width.

## 5. Open-closed Principle
> You should be able to extend the behavior of a system without having to modify that system.

**Violation 1**
```
type AuthenticationService struct {
	//
	// some fields
	//
}

func (s *AuthenticationService) Authenticate(ctx *gin.Context) (*User, error) {
	switch ctx.GetString("authType") {
	case "bearer":
		return c.authenticateWithBearerToken(ctx.Request.Header)
	case "basic":
		return c.authenticateWithBasicAuth(ctx.Request.Header)
	case "applicationKey":
		return c.authenticateWithApplicationKey(ctx.Query("applicationKey"))
	}

	return nil, errors.New("unrecognized authentication type")
}

func (s *AuthenticationService) authenticateWithApplicationKey(key string) (*User, error) {
	//
	// authenticate User from Application Key
	//
}

func (s *AuthenticationService) authenticateWithBasicAuth(h http.Header) (*User, error) {
	//
	// authenticate User from Basic Auth
	//
}

func (s *AuthenticationService) authenticateWithBearerToken(h http.Header) (*User, error) {
	//
	// validate JWT token from the request header
	//
}
```
Any changes to the authentication logic, even if it’s in a different module, require modifications in AuthenticationService.
Adding a new method of extracting an User from Context always necessitates modifications to AuthenticationService.
The logic within AuthenticationService inevitably grows with each new authentication method.

**Fixed code 1**
```
type AuthenticationProvider interface {
	Type() string
	Authenticate(ctx *gin.Context) (*User, error)
}

type AuthenticationService struct {
	providers []AuthenticationProvider
	//
	// some fields
	//
}

func (s *AuthenticationService) Authenticate(ctx *gin.Context) (*User, error) {
	for _, provider := range c.providers {
		if ctx.GetString("authType") != provider.Type() {
			continue
		}
		
		return provider.Authenticate(ctx)
	}

	return nil, errors.New("unrecognized authentication type")
}
```
In the example above, we have a candidate that adheres to the Open/Closed Principle (OCP). The struct, AuthenticationService, doesn’t conceal technical details about extracting a User from the Context. Instead, we introduced a new interface, AuthenticationProvider, which serves as the designated place for implementing various authentication logic. For instance, it can include TokenBearerProvider, ApiKeyProvider, or BasicAuthProvider. This approach allows us to centralize the logic for authorized users within one module, rather than scattering it throughout the codebase. Furthermore, we achieve our primary objective: extending AuthenticationService without needing to modify it. We can initialize AuthenticationService with as many different AuthenticationProviders as required.

**Violation 2**
```
func GetCities(sourceType string, source string) ([]City, error) {
	var data []byte
	var err error

	if sourceType == "file" {
		data, err = ioutil.ReadFile(source)
		if err != nil {
			return nil, err
		}
	} else if sourceType == "link" {
		resp, err := http.Get(source)
		if err != nil {
			return nil, err
		}

		data, err = ioutil.ReadAll(resp.Body)
		if err != nil {
			return nil, err
		}
		defer resp.Body.Close()
	}

	var cities []City
	err = yaml.Unmarshal(data, &cities)
	if err != nil {
		return nil, err
	}

	return cities, nil
}
```
The function GetCities reads the list of cities from some source. That source may be a file or some resource on the Internet. Still, we may want to read data from memory, from Redis, or any other source in the future. So somehow, it would be better to make the process of reading raw data a little more abstract. With that said, we may provide a reading strategy from the outside as a method argument.

**Fixed code 2**
```
type DataReader func(source string) ([]byte, error)

func ReadFromFile(fileName string) ([]byte, error) {
	data, err := ioutil.ReadFile(fileName)
	if err != nil {
		return nil, err
	}

	return data, nil
}

func ReadFromLink(link string) ([]byte, error) {
	resp, err := http.Get(link)
	if err != nil {
		return nil, err
	}

	data, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	return data, nil
}

func GetCities(reader DataReader, source string) ([]City, error) {
	data, err := reader(source)
	if err != nil {
		return nil, err
	}

	var cities []City
	err = yaml.Unmarshal(data, &cities)
	if err != nil {
		return nil, err
	}

	return cities, nil
}
```
As you can see in the solution above, in Go, we can define a new type that embeds a function. Here, we’ve created a new type called DataReader, which represents a function type for reading raw data from some source. The ReadFromFile and ReadFromLink methods are actual implementations of the DataReader type. 

## Dependency Injection
Using Dependency injection, we can easily pass the mocked object to the class we want to test.
E.g. assuming we want to test `populateInfo`, we would also need to mock `fetcher`
```
func populateInfo(fetcher HttpResponseFetcher, parsedInfo *Info) error {
	response, err := fetcher.Fetch("http://example.com/info")

	if err == nil {
		err = json.Unmarshal(response, parsedInfo)

		if err == nil {
			return nil
		}
	}

	return err
}
```
here we implement the mock fetcher and pass the stub into `populateInfo`
```
var infoOutput []byte = []byte(
	`{ "Environment": "production" }`
)

var statusOutput []byte = []byte(
	`{ "Status": "up" }`
)

type stubFetcher struct{}

func (fetcher stubFetcher) Fetch(url string) ([]byte, error) {
	if strings.Contains(url, "/info") {
		return infoOutput, nil
	}

	if strings.Contains(url, "/status") {
		return statusOutput, nil
	}

	return nil, errors.New("Don't recognize URL: " + url)
}
...
var info *Info
var stub stubFetcher

// We would make some assertions around this:
populateInfo(stubFetcher, info)
```


# Databases
## Transactions
Through `sql.Tx`, you can write code to execute database operations in a transaction. In a transaction, multiple operations can be performed together and conclude with a final commit, to apply all the changes in one atomic step, or a rollback, to discard them.

A database transaction groups multiple operations as part of a larger goal. All of the operations must succeed or none can, with the data’s integrity preserved in either case. Typically, a transaction workflow includes:
- Beginning the transaction.
- Performing a set of database operations.
- If no error occurs, committing the transaction to make database changes.
- If an error occurs, rolling back the transaction to leave the database unchanged.

The sql package provides methods for beginning and concluding a transaction, as well as methods for performing the intervening database operations. These methods correspond to the four steps in the workflow above.
- Begin a transaction.
    `DB.Begin` or `DB.BeginTx` begin a new database transaction, returning an sql.Tx that represents it.
- Perform database operations.
    Using an `sql.Tx`, you can query or update the database in a series of operations that use a single connection. To support this, Tx exports the following methods:
    `Exec` and `ExecContext` for making database changes through SQL statements such as INSERT, UPDATE, and DELETE.
    `Query, QueryContext, QueryRow, and QueryRowContext` for operations that return rows.
    `Prepare, PrepareContext, Stmt, and StmtContext` for pre-defining prepared statements.
- End the transaction with one of the following:
    - Commit the transaction using `Tx.Commit`.
        If Commit succeeds (returns a nil error), then all the query results are confirmed as valid and all the executed updates are applied to the database as a single atomic change. If Commit fails, then all the results from Query and Exec on the Tx should be discarded as invalid.
    - Roll back the transaction using `Tx.Rollback`.
        Even if Tx.Rollback fails, the transaction will no longer be valid, nor will it have been committed to the database.

**Best practices**
Follow the best practices below to better navigate the complicated semantics and connection management that transactions sometimes require.
- Use the APIs described in this section to manage transactions. Do not use transaction-related SQL statements such as BEGIN and COMMIT directly—doing so can leave your database in an unpredictable state, especially in concurrent programs.
- When using a transaction, take care not to call the non-transaction sql.DB methods directly, too, as those will execute outside the transaction, giving your code an inconsistent view of the state of the database or even causing deadlocks.

**Example**
Code in the following example uses a transaction to create a new customer order for an album. Along the way, the code will:
1. Begin a transaction.
2. Defer the transaction’s rollback. If the transaction succeeds, it will be committed before the function exits, making the deferred rollback call a no-op. If the transaction fails it won’t be committed, meaning that the rollback will be called as the function exits.
3. Confirm that there’s sufficient inventory for the album the customer is ordering.
4. If there’s enough, update the inventory count, reducing it by the number of albums ordered.
5. Create a new order and retrieve the new order’s generated ID for the client.
6. Commit the transaction and return the ID.

This example uses Tx methods that take a context.Context argument. This makes it possible for the function’s execution – including database operations – to be canceled if it runs too long or the client connection closes. For more, see Canceling in-progress operations.
```
// CreateOrder creates an order for an album and returns the new order ID.
func CreateOrder(ctx context.Context, albumID, quantity, custID int) (orderID int64, err error) {

    // Create a helper function for preparing failure results.
    fail := func(err error) (int64, error) {
        return 0, fmt.Errorf("CreateOrder: %v", err)
    }

    // Get a Tx for making transaction requests.
    tx, err := db.BeginTx(ctx, nil)
    if err != nil {
        return fail(err)
    }
    // Defer a rollback in case anything fails.
    // tx.Commit will get called before func exits and defer is called if everything is successful
    // and rollback will be an noop.
    defer tx.Rollback()

    // Confirm that album inventory is enough for the order.
    var enough bool
    if err = tx.QueryRowContext(ctx, "SELECT (quantity >= ?) from album where id = ?",
        quantity, albumID).Scan(&enough); err != nil {
        if err == sql.ErrNoRows {
            return fail(fmt.Errorf("no such album"))
        }
        return fail(err)
    }
    if !enough {
        return fail(fmt.Errorf("not enough inventory"))
    }

    // Update the album inventory to remove the quantity in the order.
    _, err = tx.ExecContext(ctx, "UPDATE album SET quantity = quantity - ? WHERE id = ?",
        quantity, albumID)
    if err != nil {
        return fail(err)
    }

    // Create a new row in the album_order table.
    result, err := tx.ExecContext(ctx, "INSERT INTO album_order (album_id, cust_id, quantity, date) VALUES (?, ?, ?, ?)",
        albumID, custID, quantity, time.Now())
    if err != nil {
        return fail(err)
    }
    // Get the ID of the order item just created.
    orderID, err = result.LastInsertId()
    if err != nil {
        return fail(err)
    }

    // Commit the transaction.
    if err = tx.Commit(); err != nil {
        return fail(err)
    }

    // Return the order ID.
    return orderID, nil
}
```

## Query Cancellation
You can use `context.Context` when you want the ability to cancel a database operation, such as when the client’s connection closes or the operation runs longer than you want it to.

For any database operation, you can use a database/sql package function that takes Context as an argument. Using the Context, you can specify a timeout or deadline for the operation. You can also use the Context to propagate a cancellation request through your application to the function executing an SQL statement, ensuring that resources are freed up if they’re no longer needed.

You can manage in-progress operations by using Go context.Context. A Context is a standard Go data value that can report whether the overall operation it represents has been canceled and is no longer needed. By passing a context.Context across function calls and services in your application, those can stop working early and return an error when their processing is no longer needed.

You can use a Context to set a timeout or deadline after which an operation will be canceled. To derive a Context with a timeout or deadline, call `context.WithTimeout` or `context.WithDeadline`. This allows the DB operation to be cancelled once timeout.

Code in the following timeout example derives a Context and passes it into the sql.DB QueryContext method.
```
func QueryWithTimeout(ctx context.Context) {
    // Create a Context with a timeout.
    queryCtx, cancel := context.WithTimeout(ctx, 5*time.Second)
    defer cancel()

    // Pass the timeout Context with a query.
    rows, err := db.QueryContext(queryCtx, "SELECT * FROM album")
    if err != nil {
        log.Fatal(err)
    }
    defer rows.Close()

    // Handle returned rows.
}
```

When one context is derived from an outer context, as queryCtx is derived from ctx in this example, if the outer context is canceled, then the derived context is automatically canceled as well. For example, in HTTP servers, the http.Request.Context method returns a context associated with the request. That context is canceled if the HTTP client disconnects or cancels the HTTP request (possible in HTTP/2). Passing an HTTP request’s context to QueryWithTimeout above would cause the database query to stop early either if the overall HTTP request was canceled or if the query took more than five seconds.

**Note: Always defer a call to the cancel function that’s returned when you create a new Context with a timeout or deadline.** This releases resources held by the new Context when the containing function exits. It also cancels queryCtx, but by the time the function returns, nothing should be using queryCtx anymore.


## Database connection pooling
The sql.DB database handle is safe for concurrent use by multiple goroutines (meaning the handle is what other languages might call “thread-safe”). Some other database access libraries are based on connections that can only be used for one operation at a time. To bridge that gap, each sql.DB manages a pool of active connections to the underlying database, creating new ones as needed for parallelism in your Go program.

The connection pool is suitable for most data access needs. When you call an sql.DB Query or Exec method, the sql.DB implementation retrieves an available connection from the pool or, if needed, creates one. The package returns the connection to the pool when it’s no longer needed. This supports a high level of parallelism for database access.

**Setting the maximum number of open connections**
`DB.SetMaxOpenConns` imposes a limit on the number of open connections. Past this limit, new database operations will wait for an existing operation to finish, at which time sql.DB will create another connection. By default, sql.DB creates a new connection any time all the existing connections are in use when a connection is needed.

> Keep in mind that setting a limit makes database usage similar to acquiring a lock or semaphore, with the result that your application can deadlock waiting for a new database connection.

**Setting the maximum number of idle connections**
`DB.SetMaxIdleConns` changes the limit on the maximum number of idle connections sql.DB maintains.

When an SQL operation finishes on a given database connection, it is not typically shut down immediately: the application may need one again soon, and keeping the open connection around avoids having to reconnect to the database for the next operation. By default an sql.DB keeps two idle connections at any given moment. Raising the limit can avoid frequent reconnects in programs with significant parallelism. (should be kept below file handle limit)

**Setting the maximum amount a time a connection can be idle**
`DB.SetConnMaxIdleTime` sets the maximum length of time a connection can be idle before it is closed. This causes the sql.DB to close connections that have been idle for longer than the given duration.

By default, when an idle connection is added to the connection pool, it remains there until it is needed again. When using `DB.SetMaxIdleConns` to increase the number of allowed idle connections during bursts of parallel activity, also using `DB.SetConnMaxIdleTime` can arrange to release those connections later when the system is quiet.

**Setting the maximum lifetime of connections**
Using `DB.SetConnMaxLifetime` sets the maximum length of time a connection can be held open before it is closed.

By default, a connection can be used and reused for an arbitrarily long amount of time, subject to the limits described above. In some systems, such as those using a load-balanced database server, it can be helpful to ensure that the application never uses a particular connection for too long without reconnecting.

## Preventing SQL Injection attacks
You can avoid an SQL injection risk by providing SQL parameter values as sql package function arguments. Many functions in the sql package provide parameters for the SQL statement and for values to be used in that statement’s parameters (others provide a parameter for a prepared statement and parameters).

> A prepared statement is SQL that is parsed and saved by the DBMS, typically containing placeholders but with no actual parameter values. Later, the statement can be executed with a set of parameter values.
```
// AlbumByID retrieves the specified album.
func AlbumByID(id int) (Album, error) {
    // Define a prepared statement. You'd typically define the statement
    // elsewhere and save it for use in functions such as this one.
    stmt, err := db.Prepare("SELECT * FROM album WHERE id = ?")
    if err != nil {
        log.Fatal(err)
    }

    var album Album

    // Execute the prepared statement, passing in an id value for the
    // parameter whose placeholder is ?
    err := stmt.QueryRow(id).Scan(&album.ID, &album.Title, &album.Artist, &album.Price, &album.Quantity)
    if err != nil {
        if err == sql.ErrNoRows {
            // Handle the case of no rows returned.
        }
        return album, err
    }
    return album, nil
}
```

Code in the following example uses the ? symbol as a placeholder for the id parameter, which is provided as a function argument:

```
// Correct format for executing an SQL statement with parameters.
rows, err := db.Query("SELECT * FROM user WHERE id = ?", id)
```
sql package functions that perform database operations create prepared statements from the arguments you supply. At run time, the sql package turns the SQL statement into a prepared statement and sends it along with the parameter, which is separate.

Note: Parameter placeholders vary depending on the DBMS and driver you’re using. For example, pq driver for Postgres accepts a placeholder form such as $1 instead of ?.

You might be tempted to use a function from the fmt package to assemble the SQL statement as a string with parameters included – like this:
```
// SECURITY RISK!
rows, err := db.Query(fmt.Sprintf("SELECT * FROM user WHERE id = %s", id))
```

This is not secure! When you do this, Go assembles the entire SQL statement, replacing the %s format verb with the parameter value, before sending the full statement to the DBMS. This poses an SQL injection risk because the code’s caller could send an unexpected SQL snippet as the id argument. That snippet could complete the SQL statement in unpredictable ways that are dangerous to your application.

For example, by passing a certain %s value, you might end up with something like the following, which could return all user records in your database:
```
SELECT * FROM user WHERE id = 1 OR 1=1;
```
