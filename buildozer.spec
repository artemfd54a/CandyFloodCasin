[app]

# (str) Application title
title = Candy.flood

# (str) Package name (no spaces or punctuation)
package.name = candyflood

# (str) Package domain
package.domain = org.candyflood

# (str) Source directory
source.dir = .

# (str) Files included in the application
source.include_exts = py,png,jpg,jpeg,kv,atlas,json

# (str) Application version
version = 1.0

# (list) Python dependencies
requirements = python3,kivy

# (str) Orientation
orientation = portrait

# (bool) Accept Android SDK licenses automatically in CI
android.accept_sdk_license = True

# (str) Android debug artifact
android.debug_artifact = apk

# (str) Android release artifact
android.release_artifact = aab

# (list) Android architectures
android.archs = arm64-v8a

# (int) Android API target. Leave unset so Buildozer/p4a can choose a compatible current API.
# android.api =

# (int) Minimum Android API
android.minapi = 23

# (bool) Use private app storage
android.private_storage = True

[buildozer]

# (int) 2 = debug output
log_level = 2

# (int) Do not warn about root in CI
warn_on_root = 0

# (str) Build directory
build_dir = ./.buildozer

# (str) Output directory
bin_dir = ./bin
