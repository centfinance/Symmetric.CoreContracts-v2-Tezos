const { exec } = require('child_process');

// Get the parameter passed to the npm script
const testPath = process.argv[2];

// Construct the command
const command = `PYTHONPATH="./" ~/smartpy-cli-v0.16.0/SmartPy.sh test tests/${testPath}.tests.py test-output/ --html`;

// Execute the command
exec(command, (error, stdout, stderr) => {
  if (error) {
    console.error(`exec error: ${error}`);
    return;
  }
  console.log(`stdout: ${stdout}`);
  console.error(`stderr: ${stderr}`);
});
