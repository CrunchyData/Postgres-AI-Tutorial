require 'bundler'
Bundler.require
Dotenv.load

require './db'

openai = OpenAI::Client.new(access_token: ENV['OPENAI_API_KEY'])

while recipe = DB[:recipes].where(embedding: nil).exclude(description: nil).first do
  submitted_value = recipe[:description].gsub(/\n/, ' ')

  response = openai.embeddings(
    parameters: {
      model: 'text-embedding-ada-002',
      input: submitted_value
    }
  )

  begin
    embedding_value = response["data"][0]["embedding"].to_s
    DB[:recipes].where(id: recipe[:id]).update(embedding: embedding_value)
  rescue
    puts [$!, response].inspect
  end

  sleep 1.2
end
