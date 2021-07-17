import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ComicService } from 'src/app/comic.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent implements OnInit {

  constructor(private service:ComicService, private router:Router) {     
  }

  all_comics:any=[];
  focusOnOne:boolean = false;

  onSelect(comic:any) { 
    this.router.navigate(['/sarjis', comic.name])
  }

  focusChangedHandler(comic:any) {
    this.focusOnOne = !this.focusOnOne;

    if (this.focusOnOne) {
      this.service.getComic(comic.name, comic.id).subscribe(data=>{
        this.all_comics = [data];
      });
    } else {
      this.service.getAllLatestComics().subscribe(data=>{
        this.all_comics = data;
      });  
    }
  }    

  ngOnInit(): void {
//    this.service.getAllLatestComics().subscribe(data=>{
//      this.all_comics = data;
//    });
    this.service.getAllNames().subscribe(data=>{
      this.all_comics = data;
    })
  }

}

