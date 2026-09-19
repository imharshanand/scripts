# Installing Code Runner 2 in After Effects 2026 Without Creative Cloud Desktop

## 1. Overview

This guide explains how to manually install **Code Runner 2 v2.1.0** by JakeInMotion/MotionLab into **Adobe After Effects 2026** on Windows when you **do not want to install or sign in to Adobe Creative Cloud Desktop**.

The method works by:

1. Extracting the `.zxp` extension package.
2. Installing the extracted CEP extension into Adobe's CEP extensions directory.
3. Enabling CEP debug/developer loading through the Windows Registry.
4. Restarting After Effects.
5. Loading Code Runner from **Window → Extensions**.

### Tested environment

| Component                         | Version / Path                                             |
| --------------------------------- | ---------------------------------------------------------- |
| Operating System                  | Windows 11                                                 |
| Adobe After Effects               | 2026 — **26.0.0 Build 67**                                 |
| Code Runner                       | **2.1.0**                                                  |
| Extension type                    | CEP                                                        |
| CEP Runtime declared by extension | **CSXS 11.0**                                              |
| Extension ID                      | `com.motionlab.coderunner`                                 |
| Extension directory               | `C:\Program Files (x86)\Common Files\Adobe\CEP\extensions` |
| Creative Cloud Desktop            | **Not installed / not required**                           |

---

# 2. What is Code Runner 2?

**Code Runner 2** is a CEP-based panel for After Effects that provides a convenient interface for launching things such as:

* Scripts
* Expressions
* Presets
* Menu commands
* Eases
* Custom tools/actions

The extension package is distributed as a **ZXP** file:

```text
CodeRunner2-2.1.0.zxp
```

A `.zxp` file is an Adobe CEP extension package. It is **not** an ordinary After Effects plug-in.

Therefore, putting the `.zxp` file inside:

```text
C:\Program Files\Adobe\Adobe After Effects 2026\Support Files\Plug-ins
```

does **not** install the extension.

---

# 3. Why Creative Cloud Desktop is normally involved

Adobe's traditional ZXP installation workflow often relies on Adobe's extension installation infrastructure.

For example, the ZXP Installer can attempt to communicate with After Effects and may display an error such as:

> Adobe requires that you launch the Creative Cloud desktop app and log into your Adobe account before this application can modify After Effects 2026.

This does **not** necessarily mean that CEP extensions themselves require Creative Cloud Desktop to run.

Adobe's developer documentation indicates that CEP extensions can also be installed in environments where Creative Cloud Desktop is not present, including offline/feature-restricted environments.

In this case, we bypass the Creative Cloud-dependent installer and place the CEP extension directly into Adobe's CEP extension directory.

---

# 4. Files used in this installation

The original downloaded package was located at:

```text
C:\Users\harsh\Downloads\Code_Runner_2.1.0\
```

Inside it was:

```text
CodeRunner2-2.1.0.zxp
```

The ZXP was extracted into:

```text
C:\Users\harsh\Downloads\Code_Runner_2.1.0\CodeRunner2-2.1.0-zxp-extract
```

The extracted package contained:

```text
assets
CSXS
editor
icons
jsx
main
META-INF
node_modules
starter
LICENSE.txt
THIRD-PARTY-NOTICES.txt
mimetype
```

The important part for Adobe CEP is:

```text
CSXS\manifest.xml
```

---

# 5. Verify that the package is a CEP extension

Before installing manually, inspect:

```text
CSXS\manifest.xml
```

The Code Runner 2 manifest contains:

```xml
<ExtensionManifest
    Version="6.0"
    ExtensionBundleId="com.motionlab.coderunner"
    ExtensionBundleVersion="2.1.0"
    ExtensionBundleName="Code Runner 2"
>
```

It also specifies:

```xml
<HostList>
    <Host Name="AEFT" Version="[18.0,99.9]" />
</HostList>
```

This is important because:

```text
AEFT
```

means **After Effects**.

The declared host range:

```text
[18.0,99.9]
```

includes After Effects 2026:

```text
26.0.0
```

The manifest also specifies:

```xml
<RequiredRuntimeList>
    <RequiredRuntime Name="CSXS" Version="11.0" />
</RequiredRuntimeList>
```

Therefore, the extension expects **CEP/CSXS 11**.

---

# 6. Do NOT put the ZXP in the Plug-ins folder

This is one of the most important points.

### Incorrect

Do not place:

```text
CodeRunner2-2.1.0.zxp
```

here:

```text
C:\Program Files\Adobe\Adobe After Effects 2026\Support Files\Plug-ins
```

That directory is for After Effects plug-ins such as:

```text
.aex
```

and related plug-in components.

A CEP extension is different.

### Correct location

The extension should be placed under:

```text
C:\Program Files (x86)\Common Files\Adobe\CEP\extensions
```

---

# 7. Create the Code Runner extension directory

The final installation directory used was:

```text
C:\Program Files (x86)\Common Files\Adobe\CEP\extensions\com.motionlab.coderunner
```

The folder name is based on the extension bundle ID from the manifest:

```xml
ExtensionBundleId="com.motionlab.coderunner"
```

After installation, the structure should look approximately like this:

```text
C:\Program Files (x86)\
└── Common Files
    └── Adobe
        └── CEP
            └── extensions
                ├── com.adobe.ccx.fnft-3.5.0
                ├── com.adobe.ccx.start-2.16.0
                ├── com.adobe.ccx.start-2.7.2
                └── com.motionlab.coderunner
                    ├── assets
                    ├── CSXS
                    │   └── manifest.xml
                    ├── editor
                    ├── icons
                    ├── jsx
                    ├── main
                    ├── META-INF
                    ├── node_modules
                    ├── starter
                    ├── LICENSE.txt
                    ├── THIRD-PARTY-NOTICES.txt
                    └── mimetype
```

---

# 8. Copy the extension

The easiest way is to use **Command Prompt as Administrator**.

### Step 1 — Open Administrator Command Prompt

Open Start Menu and search for:

```text
cmd
```

Right-click **Command Prompt** and select:

```text
Run as administrator
```

You should see:

```text
Administrator: Command Prompt
```

in the title bar.

---

## Step 2 — Copy the extracted extension

Run:

```cmd
robocopy "C:\Users\harsh\Downloads\Code_Runner_2.1.0\CodeRunner2-2.1.0-zxp-extract" "C:\Program Files (x86)\Common Files\Adobe\CEP\extensions\com.motionlab.coderunner" /E
```

### What this does

`robocopy` copies the complete extracted extension directory.

The `/E` option means:

> Copy all subdirectories, including empty ones.

This is preferable to manually copying individual folders because the extension contains multiple components that need to remain together.

---

# 9. Enable CEP Debug Mode

This is the key step that allows the manually extracted CEP extension to load.

Because the extension was not installed through the normal Adobe extension installation mechanism, After Effects may otherwise refuse to load it.

The Code Runner manifest specifically declares:

```xml
<RequiredRuntime Name="CSXS" Version="11.0" />
```

Therefore, the relevant registry location is:

```text
HKEY_CURRENT_USER\Software\Adobe\CSXS.11
```

Create the `PlayerDebugMode` value with:

```cmd
reg add "HKCU\Software\Adobe\CSXS.11" /v PlayerDebugMode /t REG_SZ /d 1 /f
```

You should receive something similar to:

```text
The operation completed successfully.
```

---

# 10. Verify the registry setting

Run:

```cmd
reg query "HKCU\Software\Adobe\CSXS.11" /v PlayerDebugMode
```

The expected output is:

```text
PlayerDebugMode    REG_SZ    1
```

This confirms that CEP debug mode has been enabled for the current Windows user.

---

# 11. Why CSXS.11?

It is important not to blindly use:

```text
CSXS.12
```

or another version.

The correct version is determined from the extension's manifest.

Code Runner 2 declares:

```xml
<RequiredRuntime Name="CSXS" Version="11.0" />
```

Therefore:

```text
CSXS.11
```

is the appropriate registry key for this extension.

In other words:

```text
Manifest
    ↓
RequiredRuntime = CSXS 11.0
    ↓
Registry
    ↓
HKCU\Software\Adobe\CSXS.11
```

---

# 12. Restart After Effects completely

After modifying the CEP registry setting, **After Effects must be restarted**.

If After Effects was already running:

1. Save your projects.
2. Exit After Effects.
3. Make sure the application has completely closed.
4. Start After Effects again.

For troubleshooting, it is preferable to completely close and relaunch After Effects rather than simply opening another project.

---

# 13. Open Code Runner

Once After Effects starts:

Go to:

```text
Window
    → Extensions
```

You should see entries corresponding to the Code Runner panels:

```text
Code Runner
Code Runner 2
Code Runner 3
Code Runner 4
```

The main panel is:

```text
Code Runner
```

The manifest defines the additional extensions as:

```text
com.motionlab.coderunner.slot2
com.motionlab.coderunner.slot3
com.motionlab.coderunner.slot4
```

so multiple Code Runner panels are expected.

---

# 14. Expected installation flow

The complete process can be summarized as:

```text
CodeRunner2-2.1.0.zxp
          │
          ▼
Extract ZXP
          │
          ▼
CodeRunner2-2.1.0-zxp-extract
          │
          ▼
Copy entire extension
          │
          ▼
C:\Program Files (x86)\Common Files\
Adobe\CEP\extensions\
com.motionlab.coderunner
          │
          ▼
Enable CSXS.11 PlayerDebugMode
          │
          ▼
Restart After Effects
          │
          ▼
Window → Extensions
          │
          ▼
Code Runner
```

---

# 15. Complete installation commands

For future reinstallations, the entire process can be reproduced using these two commands from an **Administrator Command Prompt**.

### Install files

```cmd
robocopy "C:\Users\harsh\Downloads\Code_Runner_2.1.0\CodeRunner2-2.1.0-zxp-extract" "C:\Program Files (x86)\Common Files\Adobe\CEP\extensions\com.motionlab.coderunner" /E
```

### Enable CEP debug mode

```cmd
reg add "HKCU\Software\Adobe\CSXS.11" /v PlayerDebugMode /t REG_SZ /d 1 /f
```

### Verify

```cmd
reg query "HKCU\Software\Adobe\CSXS.11" /v PlayerDebugMode
```

Then restart After Effects.

---

# 16. Troubleshooting

## A. Code Runner doesn't appear

First verify that the extension exists:

```cmd
dir "C:\Program Files (x86)\Common Files\Adobe\CEP\extensions\com.motionlab.coderunner"
```

Then verify the manifest:

```cmd
dir "C:\Program Files (x86)\Common Files\Adobe\CEP\extensions\com.motionlab.coderunner\CSXS"
```

You should see:

```text
manifest.xml
```

---

## B. Check the registry

Run:

```cmd
reg query "HKCU\Software\Adobe\CSXS.11" /v PlayerDebugMode
```

You need:

```text
PlayerDebugMode    REG_SZ    1
```

If it isn't present, run:

```cmd
reg add "HKCU\Software\Adobe\CSXS.11" /v PlayerDebugMode /t REG_SZ /d 1 /f
```

Then restart After Effects.

---

# 17. If the Extensions menu is greyed out

A greyed-out **Window → Extensions** menu can have several causes.

First verify that After Effects can see the CEP extension directory.

Check:

```cmd
dir "C:\Program Files (x86)\Common Files\Adobe\CEP\extensions"
```

Then:

```cmd
dir "C:\Program Files (x86)\Common Files\Adobe\CEP\extensions\com.motionlab.coderunner\CSXS"
```

If the second command returns:

```text
manifest.xml
```

the extension has been copied to the expected location.

Then verify:

```cmd
reg query "HKCU\Software\Adobe\CSXS.11" /v PlayerDebugMode
```

and restart After Effects.

---

# 18. If Code Runner opens but shows a blank/grey panel

This is different from the extension not appearing in the menu.

If the menu entry exists but the panel is blank, check:

### 1. Extension files

```cmd
dir "C:\Program Files (x86)\Common Files\Adobe\CEP\extensions\com.motionlab.coderunner\main"
```

There should be the files required by the panel, including:

```text
index.html
```

### 2. Manifest

Confirm:

```text
CSXS\manifest.xml
```

exists.

### 3. Debug mode

Confirm:

```cmd
reg query "HKCU\Software\Adobe\CSXS.11" /v PlayerDebugMode
```

returns:

```text
1
```

### 4. Restart After Effects

CEP settings are not necessarily reloaded while After Effects remains open.

---

# 19. If you accidentally install it twice

Do not create nested directories such as:

```text
com.motionlab.coderunner\
    CodeRunner2-2.1.0-zxp-extract\
        CSXS\
        main\
```

The correct structure is:

```text
com.motionlab.coderunner\
    CSXS\
    main\
    editor\
    ...
```

In particular, this file must exist directly at:

```text
C:\Program Files (x86)\Common Files\Adobe\CEP\extensions\com.motionlab.coderunner\CSXS\manifest.xml
```

**Not:**

```text
...\com.motionlab.coderunner\CodeRunner2-2.1.0-zxp-extract\CSXS\manifest.xml
```

---

# 20. Removing Code Runner

If you ever want to uninstall the manually installed extension, close After Effects and remove:

```text
C:\Program Files (x86)\Common Files\Adobe\CEP\extensions\com.motionlab.coderunner
```

You can use:

```cmd
rmdir /S /Q "C:\Program Files (x86)\Common Files\Adobe\CEP\extensions\com.motionlab.coderunner"
```

### Removing debug mode

If you enabled `PlayerDebugMode` specifically for this extension and no longer need CEP development/debug extensions, you can remove the registry value:

```cmd
reg delete "HKCU\Software\Adobe\CSXS.11" /v PlayerDebugMode /f
```

Then restart After Effects.

**Note:** If you use other manually installed CEP extensions, removing this setting may affect those extensions as well.

---

# 21. Where Code Runner stores its data

Code Runner's extension files and its user data are separate.

According to the Code Runner documentation, collection data is stored on Windows under:

```text
%APPDATA%\JakeInMotion\CodeRunner\v2\
```

This expands to approximately:

```text
C:\Users\harsh\AppData\Roaming\JakeInMotion\CodeRunner\v2\
```

Therefore, uninstalling the extension itself does not necessarily mean that your Code Runner collections/data are deleted.

---

# 22. Why this installation method works

There are three separate concepts involved:

### After Effects plug-ins

Traditional plug-ins are installed under:

```text
After Effects\Support Files\Plug-ins
```

Examples include:

```text
.aex
```

### CEP extensions

CEP extensions are installed under Adobe's CEP extension directories, such as:

```text
C:\Program Files (x86)\Common Files\Adobe\CEP\extensions
```

They contain:

```text
CSXS\manifest.xml
```

and usually HTML/JavaScript/CEF-based panel code.

### ZXP

A `.zxp` file is simply the packaged distribution format for the CEP extension.

Therefore:

```text
ZXP
 ↓
extract
 ↓
CEP extension directory
 ↓
CEP runtime
 ↓
After Effects
```

is the relevant installation chain.

---

# 23. Why the manual method was necessary in this case

The normal workflow would be roughly:

```text
ZXP
 ↓
ZXP installer
 ↓
Adobe installation infrastructure
 ↓
After Effects
```

But the ZXP installer attempted to invoke Adobe's installation mechanism and required:

```text
Creative Cloud Desktop
+
Adobe account sign-in
```

Since the requirement was explicitly to avoid Creative Cloud Desktop, the alternative was:

```text
ZXP
 ↓
manual extraction
 ↓
CEP extension directory
 ↓
CSXS.11 PlayerDebugMode
 ↓
After Effects
```

This avoids installing Creative Cloud Desktop.

---

# 24. Important distinction: Creative Cloud Desktop vs Adobe runtime

Not having Creative Cloud Desktop installed does **not** mean that After Effects cannot have its own Adobe components.

After Effects itself contains/uses the required Adobe runtime components.

The manual installation is simply avoiding the **Creative Cloud Desktop application as an extension-management interface**.

Therefore, this setup should be described as:

> **Running a CEP extension in After Effects without Creative Cloud Desktop**

rather than:

> "Installing Code Runner without any Adobe components."

After Effects itself remains an Adobe application with its own required components.

---

# 25. Security and maintenance considerations

Because this installation involves manually copying extension files into:

```text
C:\Program Files (x86)\Common Files\Adobe\CEP\extensions
```

the source of the extension matters.

For Code Runner 2, use the legitimate distribution from the developer rather than modified or repackaged copies.

The package also contains:

```text
LICENSE.txt
THIRD-PARTY-NOTICES.txt
```

which should be retained with the installation.

Do not redistribute the extracted extension as your own package if the developer's license prohibits resale/repackaging/mirroring.

---

# 26. Quick-reference checklist

For future reference:

### Before installation

* [ ] After Effects 2026 installed
* [ ] Code Runner 2.1.0 ZXP obtained from legitimate source
* [ ] After Effects closed

### Installation

* [ ] Extract ZXP
* [ ] Locate `CSXS\manifest.xml`
* [ ] Confirm `RequiredRuntime = CSXS 11.0`
* [ ] Copy extracted folder to:

```text
C:\Program Files (x86)\Common Files\Adobe\CEP\extensions\com.motionlab.coderunner
```

### Registry

Run:

```cmd
reg add "HKCU\Software\Adobe\CSXS.11" /v PlayerDebugMode /t REG_SZ /d 1 /f
```

Verify:

```cmd
reg query "HKCU\Software\Adobe\CSXS.11" /v PlayerDebugMode
```

Expected:

```text
PlayerDebugMode    REG_SZ    1
```

### Launch

* [ ] Start After Effects
* [ ] Open **Window → Extensions**
* [ ] Select **Code Runner**

### If it doesn't work

Check:

```cmd
dir "C:\Program Files (x86)\Common Files\Adobe\CEP\extensions\com.motionlab.coderunner\CSXS"
```

and:

```cmd
reg query "HKCU\Software\Adobe\CSXS.11" /v PlayerDebugMode
```

---

# 27. Final installation state

The successful configuration can ultimately be represented as:

```text
Windows 11
│
├── Adobe After Effects 2026
│   └── 26.0.0 Build 67
│
├── Adobe CEP
│   └── extensions
│       └── com.motionlab.coderunner
│           ├── CSXS
│           │   └── manifest.xml
│           ├── main
│           ├── editor
│           ├── assets
│           ├── icons
│           ├── jsx
│           ├── node_modules
│           └── starter
│
└── Registry
    └── HKCU
        └── Software
            └── Adobe
                └── CSXS.11
                    └── PlayerDebugMode = "1"
```


