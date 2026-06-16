library(shiny)
library(ggplot2)
library(bslib)

# Function to generate random DNA sequence
generate_dna <- function(length) {
  sample(c("A", "C", "G", "T"), size = length, replace = TRUE)
}

# Function to perform Chaos Game Representation
cgr <- function(sequence, iterations = 1000) {
  # Initialize coordinates
  x <- 0.5
  y <- 0.5
  
  # Define corners for each nucleotide
  corners <- list(
    A = c(0, 0),
    C = c(0, 1),
    G = c(1, 1),
    T = c(1, 0)
  )
  
  # Perform iterations
  points <- matrix(0, nrow = iterations, ncol = 2)
  for (i in 1:iterations) {
    nucleotide <- sequence[i]
    target <- corners[[nucleotide]]
    x <- (x + target[1]) / 2
    y <- (y + target[2]) / 2
    points[i,] <- c(x, y)
  }
  
  return(as.data.frame(points))
}

# UI
ui <- page_sidebar(
  title = "DNA Chaos Game Representation",
  theme = bs_theme(version = 5, bootswatch = "flatly"),
  
  sidebar = sidebar(
    sliderInput("seq_length", "DNA Sequence Length", min = 100, max = 10000, value = 1000, step = 100),
    actionButton("generate", "Generate New Sequence"),
    hr(),
    sliderInput("num_points", "Number of Points", min = 10, max = 1000, value = 10, step = 10),
    actionButton("play", "Play"),
    actionButton("stop", "Stop")
  ),
  
  plotOutput("cgr_plot"),
  
  card(
    card_header("About"),
    card_body(
      "This app demonstrates the Chaos Game Representation (CGR) for DNA sequences. 
      It generates a random DNA sequence of the specified length and plots the CGR 
      pattern. Each nucleotide (A, C, G, T) corresponds to a corner of a square, 
      and points are plotted by moving halfway from the current position to the 
      corner corresponding to each nucleotide in the sequence. Use the 'Play' button 
      to automatically increase the number of points plotted."
    )
  )
)

# Server
server <- function(input, output, session) {
  
  sequence <- reactiveVal(generate_dna(1000))
  
  observeEvent(input$generate, {
    sequence(generate_dna(input$seq_length))
    updateSliderInput(session, "num_points", value = 10)
  })
  
  # Reactive value to store the timer
  timer <- reactiveVal(NULL)
  
  # Play button functionality
  observeEvent(input$play, {
    if (is.null(timer())) {
      timer(reactiveTimer(100))  # Update every 100 ms
    }
  })
  
  # Stop button functionality
  observeEvent(input$stop, {
    if (!is.null(timer())) {
      timer(NULL)
    }
  })
  
  # Increment number of points when timer is active
  observe({
    if (!is.null(timer())) {
      timer()  # Trigger the timer
      current_value <- input$num_points
      if (current_value < 1000) {
        updateSliderInput(session, "num_points", value = current_value + 10)
      } else {
        timer(NULL)  # Stop the timer when reaching 1000 points
      }
    }
  })
  
  output$cgr_plot <- renderPlot({
    req(sequence())
    points <- cgr(sequence(), iterations = input$num_points)
    
    ggplot(points, aes(x = V1, y = V2)) +
      geom_point(size = 0.5, alpha = 0.5) +
      scale_x_continuous(limits = c(0, 1)) +
      scale_y_continuous(limits = c(0, 1)) +
      labs(title = paste("Chaos Game Representation of DNA Sequence (", input$num_points, " points)"),
           x = "X", y = "Y") +
      theme_minimal() +
      theme(aspect.ratio = 1)
  })
}

# Run the app
shinyApp(ui = ui, server = server)
