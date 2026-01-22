# iOS App Development Guide

Comprehensive guide for building iOS applications in Cursor IDE. Covers Swift/SwiftUI, Xcode setup, architecture patterns, App Store deployment, and integration with backend services.

## Overview

iOS development with:
- **Swift**: Modern programming language for iOS
- **SwiftUI**: Declarative UI framework
- **UIKit**: Traditional imperative UI framework (legacy/complex UI)
- **Xcode**: Integrated development environment
- **App Store**: Distribution and deployment

## Setup & Configuration

### Xcode Installation

```bash
# Install Xcode from Mac App Store
# Or download from developer.apple.com

# Install Command Line Tools
xcode-select --install

# Verify installation
xcodebuild -version
```

### Project Structure

```
MyApp/
├── MyApp/
│   ├── App/
│   │   ├── MyAppApp.swift          # App entry point
│   │   └── ContentView.swift       # Main view
│   ├── Models/                     # Data models
│   ├── Views/                      # SwiftUI views
│   ├── ViewModels/                 # MVVM view models
│   ├── Services/                   # API services, business logic
│   ├── Utils/                      # Utilities, extensions
│   └── Resources/
│       ├── Assets.xcassets/        # Images, colors
│       └── Info.plist              # App configuration
├── MyAppTests/                     # Unit tests
└── MyAppUITests/                   # UI tests
```

### Swift Package Manager

```swift
// Package.swift or Xcode: File → Add Package
dependencies: [
    .package(url: "https://github.com/alamofire/alamofire.git", from: "5.8.0"),
    .package(url: "https://github.com/apple/swift-log.git", from: "1.5.0"),
]
```

## SwiftUI Basics

### View Structure

```swift
import SwiftUI

struct ContentView: View {
    var body: some View {
        VStack(spacing: 20) {
            Text("Hello, World!")
                .font(.largeTitle)
            
            Button("Tap Me") {
                print("Button tapped")
            }
            .buttonStyle(.borderedProminent)
        }
        .padding()
    }
}

#Preview {
    ContentView()
}
```

### State Management

```swift
// @State for local view state
struct CounterView: View {
    @State private var count = 0
    
    var body: some View {
        VStack {
            Text("Count: \(count)")
            Button("Increment") {
                count += 1
            }
        }
    }
}

// @StateObject for view model
class CounterViewModel: ObservableObject {
    @Published var count = 0
    
    func increment() {
        count += 1
    }
}

struct CounterView: View {
    @StateObject private var viewModel = CounterViewModel()
    
    var body: some View {
        VStack {
            Text("Count: \(viewModel.count)")
            Button("Increment") {
                viewModel.increment()
            }
        }
    }
}

// @ObservedObject for passed view models
// @EnvironmentObject for shared state
```

### Navigation

```swift
// NavigationStack (iOS 16+)
struct NavigationExample: View {
    var body: some View {
        NavigationStack {
            List {
                NavigationLink("Detail", value: "detail")
                NavigationLink("Settings", value: "settings")
            }
            .navigationDestination(for: String.self) { value in
                if value == "detail" {
                    DetailView()
                } else {
                    SettingsView()
                }
            }
        }
    }
}

// Traditional NavigationLink
NavigationView {
    List {
        NavigationLink(destination: DetailView()) {
            Text("Go to Detail")
        }
    }
    .navigationTitle("Home")
}
```

### Forms & Input

```swift
struct FormExample: View {
    @State private var name = ""
    @State private var email = ""
    @State private var age = 18
    @State private var isSubscribed = false
    
    var body: some View {
        Form {
            Section("Personal Info") {
                TextField("Name", text: $name)
                TextField("Email", text: $email)
                    .keyboardType(.emailAddress)
                    .autocapitalization(.none)
            }
            
            Section("Preferences") {
                Stepper("Age: \(age)", value: $age, in: 13...100)
                Toggle("Newsletter", isOn: $isSubscribed)
            }
            
            Section {
                Button("Submit") {
                    submitForm()
                }
                .disabled(name.isEmpty || email.isEmpty)
            }
        }
    }
    
    func submitForm() {
        // Handle submission
    }
}
```

## Architecture Patterns

### MVVM (Model-View-ViewModel)

```swift
// Model
struct User: Codable, Identifiable {
    let id: UUID
    let name: String
    let email: String
}

// ViewModel
@MainActor
class UserViewModel: ObservableObject {
    @Published var users: [User] = []
    @Published var isLoading = false
    @Published var errorMessage: String?
    
    private let apiService: APIService
    
    init(apiService: APIService = APIService.shared) {
        self.apiService = apiService
    }
    
    func loadUsers() async {
        isLoading = true
        errorMessage = nil
        
        do {
            users = try await apiService.fetchUsers()
        } catch {
            errorMessage = error.localizedDescription
        }
        
        isLoading = false
    }
}

// View
struct UserListView: View {
    @StateObject private var viewModel = UserViewModel()
    
    var body: some View {
        NavigationView {
            Group {
                if viewModel.isLoading {
                    ProgressView()
                } else if let error = viewModel.errorMessage {
                    ErrorView(message: error) {
                        Task {
                            await viewModel.loadUsers()
                        }
                    }
                } else {
                    List(viewModel.users) { user in
                        UserRowView(user: user)
                    }
                }
            }
            .navigationTitle("Users")
            .task {
                await viewModel.loadUsers()
            }
        }
    }
}
```

### Repository Pattern

```swift
protocol UserRepository {
    func fetchUsers() async throws -> [User]
    func createUser(_ user: User) async throws -> User
}

class UserRepositoryImpl: UserRepository {
    private let apiService: APIService
    
    init(apiService: APIService = APIService.shared) {
        self.apiService = apiService
    }
    
    func fetchUsers() async throws -> [User] {
        return try await apiService.fetchUsers()
    }
    
    func createUser(_ user: User) async throws -> User {
        return try await apiService.createUser(user)
    }
}
```

## Networking

### URLSession

```swift
class APIService {
    static let shared = APIService()
    
    private let baseURL = "https://api.example.com"
    private let session = URLSession.shared
    
    func fetchUsers() async throws -> [User] {
        guard let url = URL(string: "\(baseURL)/users") else {
            throw APIError.invalidURL
        }
        
        let (data, response) = try await session.data(from: url)
        
        guard let httpResponse = response as? HTTPURLResponse,
              200...299 ~= httpResponse.statusCode else {
            throw APIError.invalidResponse
        }
        
        let users = try JSONDecoder().decode([User].self, from: data)
        return users
    }
    
    func createUser(_ user: User) async throws -> User {
        guard let url = URL(string: "\(baseURL)/users") else {
            throw APIError.invalidURL
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = try JSONEncoder().encode(user)
        
        let (data, response) = try await session.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse,
              200...299 ~= httpResponse.statusCode else {
            throw APIError.invalidResponse
        }
        
        let createdUser = try JSONDecoder().decode(User.self, from: data)
        return createdUser
    }
}

enum APIError: Error {
    case invalidURL
    case invalidResponse
    case decodingError(Error)
}
```

### With Authentication

```swift
extension APIService {
    private var authToken: String? {
        UserDefaults.standard.string(forKey: "authToken")
    }
    
    private func createRequest(url: URL, method: String = "GET") -> URLRequest {
        var request = URLRequest(url: url)
        request.httpMethod = method
        
        if let token = authToken {
            request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        }
        
        return request
    }
}
```

## Data Persistence

### UserDefaults

```swift
// Simple key-value storage
class UserPreferences {
    static let shared = UserPreferences()
    
    private let defaults = UserDefaults.standard
    
    var username: String? {
        get { defaults.string(forKey: "username") }
        set { defaults.set(newValue, forKey: "username") }
    }
    
    var isLoggedIn: Bool {
        get { defaults.bool(forKey: "isLoggedIn") }
        set { defaults.set(newValue, forKey: "isLoggedIn") }
    }
}
```

### Core Data

```swift
// Core Data Stack
import CoreData

class PersistenceController {
    static let shared = PersistenceController()
    
    let container: NSPersistentContainer
    
    init(inMemory: Bool = false) {
        container = NSPersistentContainer(name: "DataModel")
        
        if inMemory {
            container.persistentStoreDescriptions.first?.url = URL(fileURLWithPath: "/dev/null")
        }
        
        container.loadPersistentStores { description, error in
            if let error = error {
                fatalError("Core Data failed to load: \(error.localizedDescription)")
            }
        }
    }
}

// Usage in SwiftUI
struct ContentView: View {
    @Environment(\.managedObjectContext) private var viewContext
    
    var body: some View {
        // Use @FetchRequest or @ObservedObject with NSManagedObject
    }
}
```

## UI Components

### Lists

```swift
struct ListExample: View {
    let items = ["Item 1", "Item 2", "Item 3"]
    
    var body: some View {
        List(items, id: \.self) { item in
            Text(item)
        }
        .listStyle(.insetGrouped)
    }
}

// Dynamic list with actions
struct DynamicList: View {
    @State private var items = ["Item 1", "Item 2"]
    
    var body: some View {
        List {
            ForEach(items, id: \.self) { item in
                Text(item)
            }
            .onDelete(perform: deleteItems)
            .onMove(perform: moveItems)
        }
        .toolbar {
            EditButton()
        }
    }
    
    func deleteItems(at offsets: IndexSet) {
        items.remove(atOffsets: offsets)
    }
    
    func moveItems(from source: IndexSet, to destination: Int) {
        items.move(fromOffsets: source, toOffset: destination)
    }
}
```

### Alerts & Sheets

```swift
struct AlertExample: View {
    @State private var showAlert = false
    @State private var showConfirmation = false
    
    var body: some View {
        VStack {
            Button("Show Alert") {
                showAlert = true
            }
            
            Button("Show Confirmation") {
                showConfirmation = true
            }
        }
        .alert("Important", isPresented: $showAlert) {
            Button("OK") { }
            Button("Cancel", role: .cancel) { }
        } message: {
            Text("This is an alert message")
        }
        .confirmationDialog("Delete Item?", isPresented: $showConfirmation, titleVisibility: .visible) {
            Button("Delete", role: .destructive) {
                // Delete action
            }
            Button("Cancel", role: .cancel) { }
        }
    }
}

struct SheetExample: View {
    @State private var showSheet = false
    
    var body: some View {
        Button("Show Sheet") {
            showSheet = true
        }
        .sheet(isPresented: $showSheet) {
            SheetContentView()
        }
    }
}
```

### TabView

```swift
struct TabViewExample: View {
    var body: some View {
        TabView {
            HomeView()
                .tabItem {
                    Label("Home", systemImage: "house")
                }
            
            ProfileView()
                .tabItem {
                    Label("Profile", systemImage: "person")
                }
            
            SettingsView()
                .tabItem {
                    Label("Settings", systemImage: "gearshape")
                }
        }
    }
}
```

## Error Handling

```swift
enum AppError: LocalizedError {
    case networkError(Error)
    case decodingError(Error)
    case authenticationError
    case unknown
    
    var errorDescription: String? {
        switch self {
        case .networkError(let error):
            return "Network error: \(error.localizedDescription)"
        case .decodingError(let error):
            return "Failed to decode: \(error.localizedDescription)"
        case .authenticationError:
            return "Authentication failed"
        case .unknown:
            return "An unknown error occurred"
        }
    }
}

// Usage
do {
    let users = try await apiService.fetchUsers()
} catch {
    if let appError = error as? AppError {
        print(appError.localizedDescription)
    } else {
        print("Unexpected error: \(error)")
    }
}
```

## App Lifecycle

```swift
// App entry point
@main
struct MyAppApp: App {
    @StateObject private var appState = AppState()
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(appState)
                .onAppear {
                    // App did launch
                }
        }
    }
}

// Scene phase monitoring
struct ContentView: View {
    @Environment(\.scenePhase) private var scenePhase
    
    var body: some View {
        Text("Content")
            .onChange(of: scenePhase) { phase in
                switch phase {
                case .background:
                    // App moved to background
                case .inactive:
                    // App became inactive
                case .active:
                    // App became active
                @unknown default:
                    break
                }
            }
    }
}
```

## App Store Deployment

### App Configuration

```xml
<!-- Info.plist -->
<key>CFBundleDisplayName</key>
<string>My App</string>
<key>CFBundleIdentifier</key>
<string>com.company.myapp</string>
<key>CFBundleVersion</key>
<string>1</string>
<key>CFBundleShortVersionString</key>
<string>1.0.0</string>
```

### Build Settings

1. **Signing & Capabilities**
   - Team: Select your Apple Developer Team
   - Bundle Identifier: `com.company.myapp`
   - Capabilities: Add required capabilities (Push Notifications, etc.)

2. **Build Configuration**
   - Development: Debug build
   - Release: Optimized build for App Store

### Archive & Upload

```bash
# Build archive
xcodebuild -workspace MyApp.xcworkspace \
           -scheme MyApp \
           -configuration Release \
           -archivePath MyApp.xcarchive \
           archive

# Or use Xcode: Product → Archive

# Upload to App Store Connect
# Xcode: Window → Organizer → Distribute App
```

### Version Management

```swift
// Version in code
struct AppVersion {
    static let version = Bundle.main.infoDictionary?["CFBundleShortVersionString"] as? String ?? "Unknown"
    static let build = Bundle.main.infoDictionary?["CFBundleVersion"] as? String ?? "Unknown"
}
```

## Testing

### Unit Tests

```swift
import XCTest
@testable import MyApp

class UserViewModelTests: XCTestCase {
    var viewModel: UserViewModel!
    var mockAPIService: MockAPIService!
    
    override func setUp() {
        super.setUp()
        mockAPIService = MockAPIService()
        viewModel = UserViewModel(apiService: mockAPIService)
    }
    
    func testLoadUsers() async {
        // Given
        let expectedUsers = [User(id: UUID(), name: "Test", email: "test@example.com")]
        mockAPIService.mockUsers = expectedUsers
        
        // When
        await viewModel.loadUsers()
        
        // Then
        XCTAssertEqual(viewModel.users.count, 1)
        XCTAssertEqual(viewModel.users.first?.name, "Test")
    }
}
```

### UI Tests

```swift
import XCTest

class MyAppUITests: XCTestCase {
    var app: XCUIApplication!
    
    override func setUp() {
        super.setUp()
        app = XCUIApplication()
        app.launch()
    }
    
    func testLoginFlow() {
        let emailField = app.textFields["email"]
        emailField.tap()
        emailField.typeText("test@example.com")
        
        let passwordField = app.secureTextFields["password"]
        passwordField.tap()
        passwordField.typeText("password123")
        
        app.buttons["Login"].tap()
        
        XCTAssertTrue(app.otherElements["dashboard"].waitForExistence(timeout: 5))
    }
}
```

## Best Practices

### 1. Async/Await

Use async/await for asynchronous operations:

```swift
// GOOD
func fetchData() async throws -> Data {
    let (data, _) = try await URLSession.shared.data(from: url)
    return data
}

// AVOID callbacks where possible
```

### 2. Main Actor

Ensure UI updates on main thread:

```swift
@MainActor
class ViewModel: ObservableObject {
    @Published var isLoading = false // Automatically on main thread
}

// Or manually
Task { @MainActor in
    self.isLoading = true
}
```

### 3. Property Wrappers

```swift
// @Published for ObservableObject
// @State for local view state
// @StateObject for view-owned view models
// @ObservedObject for passed view models
// @EnvironmentObject for shared state
// @Binding for two-way data binding
```

### 4. Error Handling

Always handle errors gracefully:

```swift
func loadData() async {
    do {
        let data = try await apiService.fetchData()
        // Handle success
    } catch {
        // Handle error - show alert, log, etc.
        errorMessage = error.localizedDescription
    }
}
```

### 5. Memory Management

- Use `weak` or `unowned` for closures to avoid retain cycles
- Use `@StateObject` instead of `@ObservedObject` when creating view models
- Properly cancel tasks on view disappear

```swift
struct DataView: View {
    @StateObject private var viewModel = DataViewModel()
    @State private var task: Task<Void, Never>?
    
    var body: some View {
        Text("Data")
            .task {
                await viewModel.loadData()
            }
            .onDisappear {
                task?.cancel()
            }
    }
}
```

## Checklist for iOS Development

Before submitting to App Store:

- [ ] App properly configured (Bundle ID, version, display name)
- [ ] Signing & capabilities configured
- [ ] Required permissions in Info.plist (camera, location, etc.)
- [ ] App icon and launch screen added
- [ ] Error handling for network requests
- [ ] Loading states for async operations
- [ ] Accessibility labels for UI elements
- [ ] Dark mode support (if applicable)
- [ ] Unit tests written for critical logic
- [ ] UI tests for key user flows
- [ ] Memory leaks checked (Instruments)
- [ ] Performance tested on real devices
- [ ] Privacy policy URL configured (if collecting data)
- [ ] App Store screenshots and descriptions prepared
