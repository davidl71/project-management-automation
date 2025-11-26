const {
  sentryWebpackPlugin
} = require("@sentry/webpack-plugin");

const path = require("path");
const HTMLPlugin = require("html-webpack-plugin");

const webpack = require("webpack"); // only add this if you don't have yet

// replace accordingly './.env' with the path of your .env file
require("dotenv").config({ path: "../.env" });

module.exports = {
  entry: {
    index: "./src/index.tsx",
    //login: "./src/login.tsx",
    serviceWorker: "./src/serviceWorker.ts",
    // content scripts
    schwab: "./src/schwab.ts",
    fidelity: "./src/fidelity.ts",
    sac: "./src/sac.ts",
  },

  mode: "production",

  /*optimization: {
    minimize: false,
  },*/ // debug only
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: [
          {
            loader: "ts-loader",
            options: {
              compilerOptions: { noEmit: false },
            },
          },
        ],
        exclude: /node_modules/,
      },
      {
        exclude: /node_modules/,
        test: /\.css$/i,
        use: ["style-loader", "css-loader"],
      },
    ],
  },

  plugins: [new webpack.DefinePlugin({
    "process.env": JSON.stringify(process.env),
  }), ...getHtmlPlugins(["index" /*, "login"*/]), sentryWebpackPlugin({
    authToken: process.env.SENTRY_AUTH_TOKEN,
    org: "syntheticfi",
    project: "chrome-extension-scripts"
  })],

  resolve: {
    extensions: [".tsx", ".ts", ".js"],
  },

  output: {
    path: path.join(__dirname, "dist/"),
    filename: "[name].js",
  },

  devtool: "source-map"
};

function getHtmlPlugins(chunks) {
  return chunks.map(
    (chunk) =>
      new HTMLPlugin({
        title: "React extension",
        filename: `${chunk}.html`,
        chunks: [chunk],
      })
  );
}