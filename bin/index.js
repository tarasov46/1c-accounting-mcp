#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

// Логотип
console.log(`
1C Accounting MCP Server
========================
Organization: @tarasov46
Starting MCP server for 1C Enterprise Accounting...
`);

// Путь к Python серверу
const serverPath = path.join(__dirname, '..', 'src', 'server.py');

// Проверяем наличие Python сервера
if (!fs.existsSync(serverPath)) {
    console.error('ERROR: Python server not found at:', serverPath);
    process.exit(1);
}

// Функция поиска Python
function findPython() {
    const pythonCommands = ['python3', 'python'];
    
    for (const cmd of pythonCommands) {
        try {
            const { execSync } = require('child_process');
            const version = execSync(`${cmd} --version 2>&1`, { 
                encoding: 'utf8',
                timeout: 5000
            });
            
            if (version.includes('Python 3')) {
                console.log(`Found Python: ${cmd} (${version.trim()})`);
                return cmd;
            }
        } catch (error) {
            continue;
        }
    }
    return null;
}

// Проверка и установка зависимостей Python
async function setupPythonEnvironment() {
    const pythonCmd = findPython();
    if (!pythonCmd) {
        console.error('ERROR: Python 3 not found. Please install Python 3.8+');
        console.error('Download from: https://python.org');
        process.exit(1);
    }

    const requirementsPath = path.join(__dirname, '..', 'requirements.txt');
    
    if (fs.existsSync(requirementsPath)) {
        console.log('Checking Python dependencies for 1C MCP server...');
        
        try {
            // Проверяем ключевые зависимости
            const { execSync } = require('child_process');
            execSync(`${pythonCmd} -c "import mcp.server.fastmcp; print('MCP OK')"`, { 
                stdio: 'pipe',
                timeout: 10000
            });
            console.log('Python dependencies are installed');
        } catch (error) {
            console.log('Installing Python dependencies for 1C integration...');
            console.log('This may take a few moments...');
            
            try {
                execSync(`${pythonCmd} -m pip install -r "${requirementsPath}"`, {
                    stdio: 'inherit',
                    timeout: 120000
                });
                console.log('Dependencies installed successfully');
            } catch (installError) {
                console.error('ERROR: Failed to install Python dependencies');
                console.error('Please run manually:');
                console.error(`  ${pythonCmd} -m pip install -r requirements.txt`);
                process.exit(1);
            }
        }
    }
    
    return pythonCmd;
}

// Основная функция
async function main() {
    try {
        console.log('Setting up Python environment for 1C MCP server...');
        const pythonCmd = await setupPythonEnvironment();
        
        console.log('Starting 1C Accounting MCP server in stdio mode...');
        console.log('Available tools: hello_1c, test_calculation, generate_test_data');
        console.log('Press Ctrl+C to stop');
        console.log('');
        
        // Запуск Python сервера
        const pythonProcess = spawn(pythonCmd, [serverPath], {
            stdio: ['inherit', 'inherit', 'inherit'],
            cwd: path.join(__dirname, '..'),
            env: {
                ...process.env,
                PYTHONPATH: path.join(__dirname, '..')
            }
        });

        // Обработка сигналов для корректного завершения
        process.on('SIGINT', () => {
            console.log('\nShutting down 1C MCP server...');
            pythonProcess.kill('SIGTERM');
            setTimeout(() => {
                pythonProcess.kill('SIGKILL');
            }, 5000);
        });

        process.on('SIGTERM', () => {
            pythonProcess.kill('SIGTERM');
        });

        pythonProcess.on('close', (code) => {
            if (code !== 0 && code !== null) {
                console.error(`ERROR: 1C MCP server exited with code ${code}`);
                process.exit(code);
            }
            console.log('1C MCP server stopped gracefully');
        });

        pythonProcess.on('error', (error) => {
            console.error('ERROR: Failed to start 1C MCP server:', error.message);
            process.exit(1);
        });

    } catch (error) {
        console.error('ERROR:', error.message);
        process.exit(1);
    }
}

// Запуск
if (require.main === module) {
    main().catch(error => {
        console.error('ERROR: Unexpected error:', error);
        process.exit(1);
    });
}
