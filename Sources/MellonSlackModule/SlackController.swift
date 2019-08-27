import Vapor
import MellonCommon

/// Controls basic CRUD operations on `Todo`s.
public final class SlackController : RouteCollection {
    public init() {

    }

public func boot(router : Router) throws {
    let group = router.grouped("api", Constants.CURRENT_API_VERSION, "slack")

        group.post("interact", use: interact)
        // group.post("events", use: events)

}

    // TODO:
    func interact(_ req : Request) throws -> HTTPStatus {
        // return req.content.decode(to: HTTPStatus.self) {
            return .noContent
        // }
    }

    // TODO:
    // func events(_: Request) throws -> Empty {
    //     return flatMap(to: Empty.self)
    // }
}
