class SnakeGame < Formula
  include Language::Python::Virtualenv

  desc "Clean, minimal terminal snake game"
  url "https://github.com/navthings/snake-game/archive/refs/tags/v1.0.0.tar.gz"
  sha256 "0019dfc4b32d63c1392aa264aed2253c1e0c2fb09216f8e2cc269bbfb8bb49b5"
  license "MIT"

  depends_on "python@3.12"

  def install
    virtualenv_install_with_resources
  end

  test do
    assert_match "usage", shell_output("#{bin}/snake --help")
    assert_match version.to_s, shell_output("#{bin}/snake --version")
  end
end
