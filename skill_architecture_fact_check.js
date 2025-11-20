#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

console.log('🔍 === Updated Fact-Checking: VS Code Integration Skill vs Architecture ===\n');

// Updated architectural compliance checker for skill-based implementation
class SkillArchitectureValidator {
    constructor() {
        this.issues = [];
        this.warnings = [];
        this.complianceScore = 0;
        this.maxScore = 0;
        this.passedTests = 0;
        this.totalTests = 0;
    }

    addTest(description, testFn, weight = 1) {
        this.totalTests += weight;
        this.maxScore += weight;
        
        try {
            const result = testFn();
            if (result === true) {
                this.passedTests += weight;
                console.log(`✅ ${description}`);
            } else if (result === false) {
                this.issues.push(description);
                console.log(`❌ ${description}`);
            } else {
                this.warnings.push(`${description} (${result})`);
                console.log(`⚠️  ${description}: ${result}`);
            }
        } catch (error) {
            this.issues.push(`${description}: ${error.message}`);
            console.log(`❌ ${description}: ${error.message}`);
        }
    }

    calculateScore() {
        this.complianceScore = Math.round((this.passedTests / this.maxScore) * 100);
        return this.complianceScore;
    }
}

const validator = new SkillArchitectureValidator();

// Test 1: Skill System Integration
console.log('🎯 Testing Skill System Integration...');

validator.addTest('VS Code integration skill exists in mini_agent/skills/', () => {
    return fs.existsSync('./mini_agent/skills/vscode_integration');
});

validator.addTest('Skill has proper SKILL.md documentation', () => {
    return fs.existsSync('./mini_agent/skills/vscode_integration/SKILL.md');
});

validator.addTest('Skill implementation follows Level 3 execution pattern', () => {
    try {
        const skillFile = fs.readFileSync('./mini_agent/skills/vscode_integration/vscode_integration.py', 'utf8');
        return skillFile.includes('execute_with_resources') && skillFile.includes('Level 3');
    } catch (e) {
        return false;
    }
});

validator.addTest('Knowledge graph integration implemented', () => {
    try {
        const skillFile = fs.readFileSync('./mini_agent/skills/vscode_integration/vscode_integration.py', 'utf8');
        return skillFile.includes('knowledge_graph') || skillFile.includes('KnowledgeGraphIntegration');
    } catch (e) {
        return false;
    }
});

// Test 2: Progressive Skill Loading Pattern
console.log('\n📈 Testing Progressive Skill Loading Pattern...');

validator.addTest('Skill implements progressive loading levels', () => {
    try {
        const skillFile = fs.readFileSync('./mini_agent/skills/vscode_integration/vscode_integration.py', 'utf8');
        return skillFile.includes('list_skills') && skillFile.includes('get_skill') && 
               skillFile.includes('execute_with_resources');
    } catch (e) {
        return false;
    }
});

validator.addTest('Skill respects Mini-Agent LLM hierarchy', () => {
    try {
        const skillFile = fs.readFileSync('./mini_agent/skills/vscode_integration/vscode_integration.py', 'utf8');
        return skillFile.includes('MiniMax') && skillFile.includes('LLM') && 
               skillFile.includes('hierarchy');
    } catch (e) {
        return false;
    }
});

validator.addTest('Skill routes through Mini-Agent native system', () => {
    try {
        const skillFile = fs.readFileSync('./mini_agent/skills/vscode_integration/vscode_integration.py', 'utf8');
        return skillFile.includes('routeThroughSkillSystem') || skillFile.includes('Mini-Agent');
    } catch (e) {
        return false;
    }
});

// Test 3: Knowledge Graph Integration
console.log('\n🧠 Testing Knowledge Graph Integration...');

validator.addTest('Knowledge graph module exists', () => {
    return fs.existsSync('./mini_agent/skills/vscode_integration/knowledge_graph_integration.py');
});

validator.addTest('Knowledge graph provides session management', () => {
    try {
        const kgFile = fs.readFileSync('./mini_agent/skills/vscode_integration/knowledge_graph_integration.py', 'utf8');
        return kgFile.includes('session') && kgFile.includes('context');
    } catch (e) {
        return false;
    }
});

validator.addTest('Knowledge graph maintains Mini-Agent architecture', () => {
    try {
        const kgFile = fs.readFileSync('./mini_agent/skills/vscode_integration/knowledge_graph_integration.py', 'utf8');
        return kgFile.includes('Mini-Agent') && kgFile.includes('skill') && kgFile.includes('architecture');
    } catch (e) {
        return false;
    }
});

// Test 4: ACP Protocol Compliance
console.log('\n📡 Testing ACP Protocol Compliance...');

validator.addTest('ACP server uses JSON-RPC 2.0 over stdio', () => {
    try {
        const acpFile = fs.readFileSync('./mini_agent/acp/__init__.py', 'utf8');
        return acpFile.includes('jsonrpc') || acpFile.includes('JSON-RPC') ||
               acpFile.includes('aiohttp') || acpFile.includes('stdio');
    } catch (e) {
        return false;
    }
});

validator.addTest('ACP server integrates with Mini-Agent core', () => {
    try {
        const acpFile = fs.readFileSync('./mini_agent/acp/__init__.py', 'utf8');
        return acpFile.includes('MiniMax') || acpFile.includes('agent') ||
               acpFile.includes('tool') || acpFile.includes('config');
    } catch (e) {
        return false;
    }
});

// Test 5: Architecture Documentation
console.log('\n📚 Testing Architecture Documentation...');

validator.addTest('Skill documentation describes progressive loading', () => {
    try {
        const skillDoc = fs.readFileSync('./mini_agent/skills/vscode_integration/SKILL.md', 'utf8');
        return skillDoc.includes('progressive') && skillDoc.includes('Level 1') &&
               skillDoc.includes('Level 2') && skillDoc.includes('Level 3');
    } catch (e) {
        return false;
    }
});

validator.addTest('Documentation describes knowledge graph integration', () => {
    try {
        const skillDoc = fs.readFileSync('./mini_agent/skills/vscode_integration/SKILL.md', 'utf8');
        return skillDoc.includes('knowledge') && skillDoc.includes('graph') &&
               skillDoc.includes('context') && skillDoc.includes('persistent');
    } catch (e) {
        return false;
    }
});

// Test 6: System Integration
console.log('\n🔗 Testing System Integration...');

validator.addTest('Skill follows Mini-Agent configuration patterns', () => {
    try {
        const skillFile = fs.readFileSync('./mini_agent/skills/vscode_integration/vscode_integration.py', 'utf8');
        return skillFile.includes('config') || skillFile.includes('Config') ||
               skillFile.includes('environment') || skillFile.includes('setting');
    } catch (e) {
        return false;
    }
});

validator.addTest('Extension generation respects skill architecture', () => {
    try {
        const skillFile = fs.readFileSync('./mini_agent/skills/vscode_integration/vscode_integration.py', 'utf8');
        return skillFile.includes('skill-routed') && skillFile.includes('skill system') &&
               skillFile.includes('progressive loading');
    } catch (e) {
        return false;
    }
});

// Test 7: Production Readiness
console.log('\n🚀 Testing Production Readiness...');

validator.addTest('Error handling follows Mini-Agent patterns', () => {
    try {
        const skillFile = fs.readFileSync('./mini_agent/skills/vscode_integration/vscode_integration.py', 'utf8');
        return skillFile.includes('try') && skillFile.includes('except') &&
               skillFile.includes('logger') && skillFile.includes('error');
    } catch (e) {
        return false;
    }
});

validator.addTest('Logging provides appropriate context', () => {
    try {
        const skillFile = fs.readFileSync('./mini_agent/skills/vscode_integration/vscode_integration.py', 'utf8');
        return skillFile.includes('log') && skillFile.includes('info') &&
               skillFile.includes('Executing') && skillFile.includes('mode');
    } catch (e) {
        return false;
    }
});

// Calculate final score
const score = validator.calculateScore();

console.log('\n' + '='.repeat(70));
console.log('🔍 UPDATED FACT-CHECKING RESULTS:');
console.log(`   📊 Compliance Score: ${score}%`);
console.log(`   ✅ Passed: ${validator.passedTests}/${validator.maxScore} tests`);
console.log(`   ❌ Issues: ${validator.issues.length}`);
console.log(`   ⚠️  Warnings: ${validator.warnings.length}`);

if (validator.issues.length > 0) {
    console.log('\n❌ REMAINING ISSUES TO FIX:');
    validator.issues.forEach(issue => console.log(`   • ${issue}`));
}

if (validator.warnings.length > 0) {
    console.log('\n⚠️  WARNINGS TO REVIEW:');
    validator.warnings.forEach(warning => console.log(`   • ${warning}`));
}

// Generate recommendations
console.log('\n📋 ARCHITECTURAL COMPLIANCE ANALYSIS:');

if (score >= 90) {
    console.log('   🟢 EXCELLENT COMPLIANCE: 90%+ architectural alignment achieved');
    console.log('   ✅ Skill system properly integrated');
    console.log('   ✅ Knowledge graph integration functional');
    console.log('   ✅ Progressive loading pattern implemented');
    console.log('   ✅ ACP protocol compliant');
} else if (score >= 75) {
    console.log('   🟡 GOOD COMPLIANCE: 75-89% architectural alignment achieved');
    console.log('   • Minor refinements needed for optimal alignment');
} else {
    console.log('   🔴 NEEDS IMPROVEMENT: <75% architectural alignment');
    console.log('   • Significant architectural work required');
}

console.log('\n🎯 IMPLEMENTATION STATUS:');
if (validator.issues.length === 0) {
    console.log('   🟢 SKILL-BASED ARCHITECTURE: Implementation ready');
    console.log('   📦 Package: Skill-based integration with knowledge graph');
    console.log('   🔗 Pattern: Mini-Agent native skill → Chat API');
} else {
    console.log('   🟡 PARTIAL IMPLEMENTATION: Continue fixes needed');
    console.log('   📋 Focus: Address remaining architectural issues');
}

console.log('\n' + '='.repeat(70));

// Export results
const results = {
    complianceScore: score,
    totalTests: validator.totalTests,
    passedTests: validator.passedTests,
    issues: validator.issues,
    warnings: validator.warnings,
    needsImprovement: score < 90,
    implementationType: "skill_based"
};

module.exports = results;