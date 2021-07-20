import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { ComicService } from '../comic.service';

@Component({
  selector: 'app-comic-list',
  templateUrl: './comic-list.component.html',
  styleUrls: ['./comic-list.component.css']
})
export class ComicListComponent implements OnInit {

  all_comics:any=[];
  errors:any=[];

  constructor(private service:ComicService) { }

  ngOnInit(): void {
    var names:any=[]
    this.service.getAllNames().subscribe( data => {
      names = data;
      var i:string;
      for (i in names) {
        this.service.getLatestComic(names[i].name).subscribe(
           data => {
            this.all_comics.push(data);
          },
          error => {
            this.errors.push(names[i].name);
          }
        );
      }
    });


  }
    
}
