// Cuts the subject out of each photo with Apple's Vision framework (runs on this Mac, nothing uploaded).
// Usage: birdmask <out dir> <photo> [<photo> ...]
// For each photo writes <out>/<name>.labels.png (one grey level per separate subject, model resolution)
// and <out>/<name>.mask.png (soft mask of the biggest subject, full photo size), and prints a JSON line:
// {"file":..., "subjects":N, "areas":[fraction of the photo for each subject]}
import Foundation
import Vision
import CoreImage
import ImageIO
import UniformTypeIdentifiers

let args = CommandLine.arguments
let outDir = URL(fileURLWithPath: args[1])
let ctx = CIContext()

func writePNG(_ img: CIImage, _ url: URL, gray: Bool) {
    let cs = gray ? CGColorSpaceCreateDeviceGray() : CGColorSpaceCreateDeviceRGB()
    guard let cg = ctx.createCGImage(img, from: img.extent, format: gray ? .L8 : .RGBA8, colorSpace: cs),
          let dst = CGImageDestinationCreateWithURL(url as CFURL, UTType.png.identifier as CFString, 1, nil) else { return }
    CGImageDestinationAddImage(dst, cg, nil); CGImageDestinationFinalize(dst)
}

for path in args.dropFirst(2) {
    let url = URL(fileURLWithPath: path), name = url.deletingPathExtension().lastPathComponent
    let req = VNGenerateForegroundInstanceMaskRequest()
    let handler = VNImageRequestHandler(url: url, options: [:])
    do { try handler.perform([req]) } catch { print("{\"file\":\"\(name)\",\"error\":\"vision\"}"); continue }
    guard let obs = req.results?.first else { print("{\"file\":\"\(name)\",\"subjects\":0,\"areas\":[]}"); continue }
    // label map: count pixels per subject
    let lm = obs.instanceMask
    CVPixelBufferLockBaseAddress(lm, .readOnly)
    let w = CVPixelBufferGetWidth(lm), h = CVPixelBufferGetHeight(lm), rb = CVPixelBufferGetBytesPerRow(lm)
    let base = CVPixelBufferGetBaseAddress(lm)!.assumingMemoryBound(to: UInt8.self)
    var counts = [Int: Int]()
    for y in 0..<h { for x in 0..<w { let v = Int(base[y * rb + x]); if v > 0 { counts[v, default: 0] += 1 } } }
    CVPixelBufferUnlockBaseAddress(lm, .readOnly)
    let ids = obs.allInstances.sorted { (counts[$0] ?? 0) > (counts[$1] ?? 0) }
    let areas = ids.map { String(format: "%.4f", Double(counts[$0] ?? 0) / Double(w * h)) }
    // labels scaled up so they're visible: subject k -> grey 40*k
    let li = CIImage(cvPixelBuffer: lm).applyingFilter("CIColorMatrix", parameters: [
        "inputRVector": CIVector(x: 40, y: 0, z: 0, w: 0), "inputGVector": CIVector(x: 40, y: 0, z: 0, w: 0),
        "inputBVector": CIVector(x: 40, y: 0, z: 0, w: 0)])
    writePNG(li, outDir.appendingPathComponent(name + ".labels.png"), gray: true)
    if let big = ids.first, let m = try? obs.generateScaledMaskForImage(forInstances: IndexSet(integer: big), from: handler) {
        writePNG(CIImage(cvPixelBuffer: m), outDir.appendingPathComponent(name + ".mask.png"), gray: true)
    }
    print("{\"file\":\"\(name)\",\"subjects\":\(ids.count),\"ids\":\(ids.map{$0}),\"areas\":[\(areas.joined(separator: ","))]}")
    fflush(stdout)
}
