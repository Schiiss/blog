# Local dev only, loaded via RUBYOPT in the Dockerfile.
# WEBrick answers a Range request that carries a matching If-None-Match with an
# empty 304 instead of the requested bytes, which breaks <video> playback in Chrome.
require "webrick"

WEBrick::HTTPServlet::DefaultFileHandler.prepend(Module.new do
  def not_modified?(req, res, mtime, etag)
    return false if req["range"]
    super
  end
end)
