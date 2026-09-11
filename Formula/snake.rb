class Snake < Formula
  include Language::Python::Virtualenv

  desc "Clean, minimal terminal snake game"
  url "https://github.com/navthings/snake/archive/refs/tags/v1.0.0.tar.gz"
  sha256 "89a69bec6ea69864a3d513d41ad14f10e22a140173f6bcea4c648435db9e930f"
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
