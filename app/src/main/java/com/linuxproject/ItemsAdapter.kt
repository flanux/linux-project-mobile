package com.linuxproject

import android.content.Intent
import android.net.Uri
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView

class ItemsAdapter(private val items: List<DisplayItem>) : 
    RecyclerView.Adapter<RecyclerView.ViewHolder>() {
    
    companion object {
        const val TYPE_HEADER = 0
        const val TYPE_INTERNSHIP = 1
        const val TYPE_JOB = 2
        const val TYPE_NEWS = 3
        const val TYPE_PROJECT = 4
        const val TYPE_LEARNING = 5
    }
    
    override fun getItemViewType(position: Int): Int {
        return when (items[position]) {
            is DisplayItem.Header -> TYPE_HEADER
            is DisplayItem.Internship -> TYPE_INTERNSHIP
            is DisplayItem.Job -> TYPE_JOB
            is DisplayItem.News -> TYPE_NEWS
            is DisplayItem.Project -> TYPE_PROJECT
            is DisplayItem.Learning -> TYPE_LEARNING
        }
    }
    
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): RecyclerView.ViewHolder {
        val inflater = LayoutInflater.from(parent.context)
        return when (viewType) {
            TYPE_HEADER -> HeaderViewHolder(
                inflater.inflate(R.layout.item_header, parent, false)
            )
            TYPE_INTERNSHIP -> InternshipViewHolder(
                inflater.inflate(R.layout.item_internship, parent, false)
            )
            TYPE_JOB -> JobViewHolder(
                inflater.inflate(R.layout.item_job, parent, false)
            )
            TYPE_NEWS -> NewsViewHolder(
                inflater.inflate(R.layout.item_news, parent, false)
            )
            TYPE_PROJECT -> ProjectViewHolder(
                inflater.inflate(R.layout.item_project, parent, false)
            )
            else -> LearningViewHolder(
                inflater.inflate(R.layout.item_learning, parent, false)
            )
        }
    }
    
    override fun onBindViewHolder(holder: RecyclerView.ViewHolder, position: Int) {
        when (val item = items[position]) {
            is DisplayItem.Header -> (holder as HeaderViewHolder).bind(item)
            is DisplayItem.Internship -> (holder as InternshipViewHolder).bind(item)
            is DisplayItem.Job -> (holder as JobViewHolder).bind(item)
            is DisplayItem.News -> (holder as NewsViewHolder).bind(item)
            is DisplayItem.Project -> (holder as ProjectViewHolder).bind(item)
            is DisplayItem.Learning -> (holder as LearningViewHolder).bind(item)
        }
    }
    
    override fun getItemCount() = items.size
    
    class HeaderViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        private val titleText: TextView = view.findViewById(R.id.headerTitle)
        
        fun bind(item: DisplayItem.Header) {
            titleText.text = item.title
        }
    }
    
    class InternshipViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        private val titleText: TextView = view.findViewById(R.id.internshipTitle)
        private val orgText: TextView = view.findViewById(R.id.internshipOrg)
        private val descText: TextView = view.findViewById(R.id.internshipDesc)
        
        fun bind(item: DisplayItem.Internship) {
            titleText.text = item.title
            orgText.text = item.organization
            descText.text = item.description
            
            itemView.setOnClickListener {
                if (item.link.isNotEmpty()) {
                    val intent = Intent(Intent.ACTION_VIEW, Uri.parse(item.link))
                    itemView.context.startActivity(intent)
                }
            }
        }
    }
    
    class JobViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        private val titleText: TextView = view.findViewById(R.id.jobTitle)
        private val companyText: TextView = view.findViewById(R.id.jobCompany)
        private val locationText: TextView = view.findViewById(R.id.jobLocation)
        
        fun bind(item: DisplayItem.Job) {
            titleText.text = item.title
            companyText.text = item.company
            locationText.text = item.location
            
            itemView.setOnClickListener {
                if (item.link.isNotEmpty()) {
                    val intent = Intent(Intent.ACTION_VIEW, Uri.parse(item.link))
                    itemView.context.startActivity(intent)
                }
            }
        }
    }
    
    class NewsViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        private val titleText: TextView = view.findViewById(R.id.newsTitle)
        private val sourceText: TextView = view.findViewById(R.id.newsSource)
        private val dateText: TextView = view.findViewById(R.id.newsDate)
        
        fun bind(item: DisplayItem.News) {
            titleText.text = item.title
            sourceText.text = item.source
            dateText.text = item.date
            
            itemView.setOnClickListener {
                if (item.link.isNotEmpty()) {
                    val intent = Intent(Intent.ACTION_VIEW, Uri.parse(item.link))
                    itemView.context.startActivity(intent)
                }
            }
        }
    }
    
    class ProjectViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        private val nameText: TextView = view.findViewById(R.id.projectName)
        private val descText: TextView = view.findViewById(R.id.projectDesc)
        private val categoryText: TextView = view.findViewById(R.id.projectCategory)
        
        fun bind(item: DisplayItem.Project) {
            nameText.text = item.name
            descText.text = item.description
            categoryText.text = item.category
            
            itemView.setOnClickListener {
                if (item.link.isNotEmpty()) {
                    val intent = Intent(Intent.ACTION_VIEW, Uri.parse(item.link))
                    itemView.context.startActivity(intent)
                }
            }
        }
    }
    
    class LearningViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        private val titleText: TextView = view.findViewById(R.id.learningTitle)
        private val typeText: TextView = view.findViewById(R.id.learningType)
        private val sourceText: TextView = view.findViewById(R.id.learningSource)
        
        fun bind(item: DisplayItem.Learning) {
            titleText.text = item.title
            typeText.text = item.type
            sourceText.text = item.source
            
            itemView.setOnClickListener {
                if (item.link.isNotEmpty()) {
                    val intent = Intent(Intent.ACTION_VIEW, Uri.parse(item.link))
                    itemView.context.startActivity(intent)
                }
            }
        }
    }
}
