// swift-tools-version:4.2
import PackageDescription

let package = Package(
    name: "MellonSlackModule",
    products: [
        .library(name: "MellonSlackModule", targets: ["MellonSlackModule"]),
    ],
    dependencies: [
        .package(url: "https://github.com/vapor/vapor.git", from: "3.0.0"),
        .package(path: "../MellonCore"),
        .package(path: "../MellonCommon"),
    ],
    targets: [
        .target(name: "MellonSlackModule", dependencies: ["MellonCore", "MellonCommon", "Vapor"]),
        .testTarget(name: "MellonSlackModuleTests", dependencies: ["MellonSlackModule"]),
    ]
)
