class Snake < Formula
  include Language::Python::Virtualenv

  desc "Clean, minimal terminal snake game"
  url "https://github.com/navthings/snake/archive/refs/tags/v1.0.0.tar.gz"
  sha256 "ba549db31ece768063767f1d59b88f708ec28d7a437be304939ddea26e611dee"
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
