const commandArgsMiddleware = require('./middleware');
const {
    Telegraf,
    Context
} = require('telegraf')
const {
    ethers
} = require('ethers')

require("dotenv").config();


const bot = new Telegraf(process.env.TELE_TOKEN)
bot.use(commandArgsMiddleware())


bot.on('sticker', (ctx) => ctx.reply('👍'))
bot.hears('hi', (ctx) => ctx.reply('Hey there'))
bot.help((ctx) => ctx.reply('Send me a sticker'))
bot.command('buybox', (ctx) => {
    console.log(ctx.state.command)
})
bot.launch()