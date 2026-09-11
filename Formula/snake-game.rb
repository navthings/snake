class SnakeGame < Formula
  include Language::Python::Virtualenv

  desc "Clean, minimal terminal snake game"
  homepage "https://github.com/yourname/snake-game"
  url "https://github.com/yourname/snake-game/archive/refs/tags/v1.0.0.tar.gz"
  sha256 "REPLACE_WITH_ACTUAL_SHA256"
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
