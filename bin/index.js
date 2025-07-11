#!/usr/bin/env node

const { spawn, execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

// Убираем баннер - он мешает MCP протоколу
// console.error(`
// 1C Accounting MCP Server v1.0.1
// ===============================
// Author: tarasov46
// Starting MCP server...
// `);

function checkPythonVersion(pythonCmd) {
    try {
        const versionOutput = execSync(`${pythonCmd} --version 2>&1`, { 
            encoding: 'utf8',
            timeout: 5000
        });
        
        const versionMatch = versionOutput.match(/Python (\d+)\.(\d+)/);
        if (versionMatch) {
            const major = parseInt(versionMatch[1]);
            const minor = parseInt(versionMatch[2]);
            
            if (major > 3 || (major === 3 && minor >= 10)) {
                // console.error(`✓ Found Python: ${versionOutput.trim()}`);
                return true;
            } else {
                console.error(`✗ Python version too old: ${versionOutput.trim()}`);
                console.error(`  Required: Python >= 3.10`);
                return false;
            }
        }
        return false;
    } catch (error) {
        return false;
    }
}

function findCompatiblePython() {
    const pythonCommands = ['python3', 'python', 'python3.10', 'python3.11', 'python3.12'];
    
    for (const cmd of pythonCommands) {
        if (checkPythonVersion(cmd)) {
            return cmd;
        }
    }
    return null;
}

async function setupPythonEnvironment() {
    const pythonCmd = findCompatiblePython();
    
    if (!pythonCmd) {
        console.error(`
ERROR: Compatible Python not found!

Requirements:
- Python 3.10 or higher
- pip package manager

Installation: https://python.org/downloads/
        `);
        process.exit(1);
    }

    const requirementsPath = path.join(__dirname, '..', 'requirements.txt');
    
    if (fs.existsSync(requirementsPath)) {
        // console.error('Checking Python dependencies...');
        
        try {
            execSync(`${pythonCmd} -c "import mcp.server; print('MCP OK')"`, { 
                stdio: 'pipe',
                timeout: 10000
            });
            // console.error('✓ Dependencies installed');
        } catch (error) {
            // console.error('Installing dependencies...');
            
            try {
                const installCmd = `${pythonCmd} -m pip install -r "${requirementsPath}"`;
                execSync(installCmd, {
                    stdio: 'pipe',  // Не показываем процесс установки
                    timeout: 180000
                });
                // console.error('✓ Dependencies installed successfully');
            } catch (installError) {
                console.error(`ERROR: Failed to install dependencies`);
                console.error(`Manual install: ${pythonCmd} -m pip install -r requirements.txt`);
                process.exit(1);
            }
        }
    }
    
    return pythonCmd;
}

async function main() {
    try {
        const serverPath = path.join(__dirname, '..', 'src', 'server.py');
        if (!fs.existsSync(serverPath)) {
            console.error('ERROR: server.py not found');
            process.exit(1);
        }

        const pythonCmd = await setupPythonEnvironment();
        
        // Убираем информационные сообщения - они мешают MCP
        // console.error('Starting 1C MCP server...');
        // console.error('Tools: hello_1c, test_calculation, generate_test_data, get_server_status');
        // console.error('');
        
        const pythonProcess = spawn(pythonCmd, [serverPath], {
            stdio: 'inherit',
            cwd: path.join(__dirname, '..'),
            env: {
                ...process.env,
                PYTHONPATH: path.join(__dirname, '..', 'src'),
                PYTHONUNBUFFERED: '1'
            }
        });

        process.on('SIGINT', () => {
            // console.error('\nShutting down...');
            pythonProcess.kill('SIGTERM');
        });

        pythonProcess.on('close', (code) => {
            if (code !== 0 && code !== null) {
                console.error(`Server exited with code ${code}`);
                process.exit(code);
            }
            process.exit(0);
        });

        pythonProcess.on('error', (error) => {
            console.error('ERROR:', error.message);
            process.exit(1);
        });

    } catch (error) {
        console.error('ERROR:', error.message);
        process.exit(1);
    }
}

if (require.main === module) {
    main().catch(error => {
        console.error('ERROR:', error);
        process.exit(1);
    });
}

module.exports = { main };