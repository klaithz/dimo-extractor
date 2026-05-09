ObjC.import("Foundation");

function currentApp() {
  const app = Application.currentApplication();
  app.includeStandardAdditions = true;
  return app;
}

function bundlePath() {
  return ObjC.unwrap($.NSBundle.mainBundle.bundlePath);
}

function scriptDirectory() {
  const bundle = bundlePath();
  return ObjC.unwrap($(bundle).stringByDeletingLastPathComponent);
}

function pythonScriptPath() {
  const bundledPath = $.NSBundle.mainBundle.pathForResourceOfType(
    $("extract_dimo_quotes"),
    $("py")
  );
  if (bundledPath) {
    return ObjC.unwrap(bundledPath);
  }

  return scriptDirectory() + "/extract_dimo_quotes.py";
}

function shellQuote(text) {
  return "'" + String(text).replace(/'/g, "'\\''") + "'";
}

function isTextFile(path) {
  return String(path).toLowerCase().endsWith(".txt");
}

function joinLines(lines) {
  return lines.join("\n");
}

function run() {
  currentApp().displayDialog(
    "请把一个或多个滴墨书摘导出的 .txt 文件拖到这个应用上。"
  );
}

function openDocuments(droppedItems) {
  const app = currentApp();
  const items = droppedItems || [];
  const skipped = [];
  const validPaths = [];

  for (const item of items) {
    const itemPath = String(item);
    if (isTextFile(itemPath)) {
      validPaths.push(itemPath);
    } else {
      skipped.push("已跳过非 .txt 文件: " + itemPath);
    }
  }

  if (validPaths.length === 0) {
    let message = "没有收到可处理的 .txt 文件。";
    if (skipped.length > 0) {
      message += "\n\n" + joinLines(skipped);
    }
    app.displayDialog(message);
    return;
  }

  const command =
    "/usr/bin/python3 " +
    shellQuote(pythonScriptPath()) +
    " " +
    validPaths.map(shellQuote).join(" ");

  try {
    const result = app.doShellScript(command);
    let message = result || "处理完成。";
    if (skipped.length > 0) {
      message = joinLines(skipped) + "\n\n" + message;
    }
    app.displayDialog(message);
  } catch (error) {
    let message = "处理失败：\n" + error.toString();
    if (skipped.length > 0) {
      message = joinLines(skipped) + "\n\n" + message;
    }
    app.displayDialog(message);
  }
}
